import marimo

__generated_with = "0.14.12"
app = marimo.App()


@app.cell
def _():
    # Basic JSL document
    import json, jsl

    class TextField(jsl.StringField):
        pass

    class ExampleDocument(jsl.document.Document):
        single_str = jsl.StringField()
        str_array = jsl.ArrayField(jsl.StringField())
        text_data = TextField()
        text_array = jsl.ArrayField(TextField())
        single_int = jsl.IntField()
        int_array = jsl.ArrayField(jsl.IntField())
        single_float = jsl.NumberField()
        float_array = jsl.ArrayField(jsl.NumberField())

    # print(json.dumps(ExampleDocument.get_schema(ordered=True), indent=2))
    for field in ExampleDocument().resolve_and_iter_fields():
        print(field)
    return ExampleDocument, TextField, jsl, json


@app.cell
def _():
    expected_es_template = {
        "template": "project-example_document-template_v1_0_0-*",
        "settings": {},
        "aliases": {
            "project-example_document": {}
        },
        "mappings": {
            "content": {
                "properties": {
                    "@timestamp": {
                        "type": "date",
                        "format": "dateOptionalTime"
                    },
                    "single_str": {
                        "index": "not_analyzed",
                        "type": "string",
                        "doc_values": True
                    },
                    "str_array": {
                        "index": "not_analyzed",
                        "type": "string",
                        "doc_values": True
                    },
                    "text_data": {
                        "type": "string"
                    },
                    "text_array": {
                        "type": "string"
                    },
                    "single_float": {
                        "type": "float"
                    },
                    "float_array": {
                        "type": "float"
                    },
                    "single_int": {
                        "type": "integer"
                    },
                    "int_array": {
                        "type": "integer"
                    },
                }
            }
        }
    }
    return (expected_es_template,)


@app.cell
def _(TextField, jsl):
    # Prototype jsl-elasticsearch library implementation
    from collections import OrderedDict
    from functools import singledispatch

    @singledispatch
    def render_es_field(jsl_field, role):
        raise NotImplementedError("Unknown JSL Field type: {!r}".format(type(jsl_field)))

    @render_es_field.register(jsl.DocumentField)
    def render_document_field(jsl_field, role):
        return OrderedDict((
            ("type", "nested"),
            ("properties", get_es_properties(jsl_field.document_cls, role)),
        ))

    @render_es_field.register(jsl.DictField)
    def render_dict_field(jsl_field, role):
        properties, properties_role = jsl_field.resolve_attr('properties', role)
        result = OrderedDict()
        for name, field in sorted(properties.items()):
            result[name] = render_es_field(field, role)
        return OrderedDict((
            ("type", "nested"),
            ("properties", result),
        ))

    @render_es_field.register(jsl.ArrayField)
    def render_array_field(jsl_field, role):
        # All ElasticSearch fields are implicitly arrays
        # so just render the contained field type
        return render_es_field(jsl_field.items, role)
    
    @render_es_field.register(jsl.StringField)
    def render_string_field(jsl_field, role):
        return OrderedDict((
            ("type", "string"),
            ("index", "not_analyzed"),
            ("doc_values", True),
        ))

    @render_es_field.register(TextField)
    def render_text_field(jsl_field, role):
        return {
            "type": "string",
        }

    @render_es_field.register(jsl.IntField)
    def render_int_field(jsl_field, role):
        return {
            "type": "integer",
        }

    @render_es_field.register(jsl.NumberField)
    def render_int_field(jsl_field, role):
        return {
            "type": "float",
        }

    def get_es_properties(document, role, *, add_timestamp=False):
        result = OrderedDict()
        if add_timestamp:
            result["@timestamp"] = OrderedDict((
                ("type", "date"),
                ("format", "dateOptionalTime"),
            ))
        for name, field in document.resolve_and_iter_fields(role):
            result[name] = render_es_field(field, role)
        return result


    def make_es_template(title, version, document, doc_type="content"):
        template = "{}-template_{}-*".format(title, version.replace("-", "_"))
        settings = {}
        aliases = {
            title: {}
        }
        doc_properties = get_es_properties(document, version, add_timestamp=True)
        mappings = {
            doc_type: {
                "properties": doc_properties
            }
        }
        return OrderedDict((
            ("template", template),
            ("settings", settings),
            ("aliases", aliases),
            ("mappings", mappings),
        ))
    return (make_es_template,)


@app.cell
def _(ExampleDocument, expected_es_template, json, make_es_template):
    # Check rendering of primitive fields and arrays
    example_es_template = make_es_template("project-example_document", "v1-0-0", ExampleDocument)
    assert example_es_template == expected_es_template
    print(json.dumps(example_es_template, indent=2))
    return


@app.cell
def _(ExampleDocument, jsl, json, make_es_template):
    # Support nested documents
    class NestedDocuments(jsl.document.Document):
        single_doc = jsl.DocumentField(ExampleDocument, as_ref=True)
        doc_array = jsl.ArrayField(jsl.DocumentField(ExampleDocument, as_ref=True))
        single_dict = jsl.DictField(dict(str_key=jsl.StringField(), int_key=jsl.IntField()))
        dict_array = jsl.ArrayField(jsl.DictField(dict(str_key=jsl.StringField(), int_key=jsl.IntField())))


    nested_es_template = make_es_template("project-nested_documents", "v1-0-0", NestedDocuments)
    print(json.dumps(nested_es_template, indent=2))
    return


@app.cell
def _(jsl, json, make_es_template):
    # Support generating version specific mappings
    ROLE_v1_0_0 = "v1-0-0"
    ROLE_v2_0_0 = "v2-0-0"

    ROLE_TITLE = jsl.roles.Var({
        ROLE_v1_0_0: "MyDocument v1-0-0",
        ROLE_v2_0_0: "MyDocument v2-0-0",
    })


    class MultiversionDocument(jsl.document.Document):
        class Options(object):
            title = ROLE_TITLE

        with jsl.roles.Scope(ROLE_v1_0_0) as v1:
            v1.subfield = jsl.fields.NumberField()
        with jsl.roles.Scope(ROLE_v2_0_0) as v2:
            v2.subfield = jsl.fields.IntField()

    multiversion_v1_0_0_template = make_es_template("project-multiversion_document", "v1-0-0", MultiversionDocument)
    print(json.dumps(multiversion_v1_0_0_template, indent=2))
    return (MultiversionDocument,)


@app.cell
def _(MultiversionDocument, json, make_es_template):
    multiversion_v2_0_0_template = make_es_template("project-multiversion_document", "v2-0-0", MultiversionDocument)
    print(json.dumps(multiversion_v2_0_0_template, indent=2))
    return


@app.cell
def _(json_1):
    import uuid
    from IPython.display import display_javascript, display_html, display
    import json

    class RenderJSON(object):

        def __init__(self, json_data):
            if isinstance(json_data, dict):
                self.json_str = json_1.dumps(json_data)
            else:
                self.json_str = json_1
            self.uuid = str(uuid.uuid4())

        def _ipython_display_(self):
            display_html('<div id="{}" style="height: 600px; width:100%;"></div>'.format(self.uuid), raw=True)
            display_javascript('\n        require(["./renderjson.js"], function() {\n          renderjson.set_show_to_level(1)\n          document.getElementById(\'%s\').appendChild(renderjson(%s))\n        });\n        ' % (self.uuid, self.json_str), raw=True)
    return RenderJSON, json


@app.cell
def _(RenderJSON, expected_es_template):
    RenderJSON(expected_es_template)
    return


if __name__ == "__main__":
    app.run()
