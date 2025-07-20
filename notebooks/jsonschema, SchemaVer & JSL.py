import marimo

__generated_with = "0.14.12"
app = marimo.App()


@app.cell
def _():
    # JSON is a wonderful format that provides a lot of convenience for
    # data publishers, redistributors and consumers
    the_data = {
        "my": "amazing",
        "flexible": "but maybe",
        "not so user-friendly": "JSON-compatible data structure"
    }
    def consume(data):
        print(data["not so user-friendly"].lower())
    consume(the_data)
    return (consume,)


@app.cell
def _(consume):
    # But data models change, and communicating that to data consumers can be a problem
    the_data_in_a_new_format = {
        "my": "amazing",
        "flexible": "but maybe",
        "not so user-friendly": 1
    }
    consume(the_data_in_a_new_format)
    return


@app.cell
def _(false):
    # jsonschema to the rescue?
    my_original_schema = {
      "$schema": "http://json-schema.org/draft-04/schema#",
      "type": "object",
      "properties": {
        "my": {
          "type": "string"
        },
        "flexible": {
          "type": "string"
        },
        "not so user-friendly": {
          "type": "string"
        }
      },
      "additionalProperties": false
    }

    # Or maybe not.
    # Hard to write, hard to diff, hard to review, hard to maintain in general
    return


@app.cell
def _():
    # Enter JSL
    import json, jsl
    class MyDocument(jsl.document.Document):
        my = jsl.fields.StringField()
        flexible = jsl.fields.StringField()
        not_so_user_friendly = jsl.fields.StringField(name="not so user-friendly")


    print(json.dumps(MyDocument.get_schema(ordered=True), indent=2))
    return jsl, json


@app.cell
def _(jsl, json):
    # With SchemaVer and JSL roles for easy to maintain schema updates
    ROLE_v1_0_0 = "v1-0-0"
    ROLE_v2_0_0 = "v2-0-0"

    ROLE_TITLE = jsl.roles.Var({
        ROLE_v1_0_0: "MyDocument v1-0-0",
        ROLE_v2_0_0: "MyDocument v2-0-0",
    })


    class MyMultiformatDocument(jsl.document.Document):
        class Options(object):
            title = ROLE_TITLE

        my = jsl.fields.StringField()
        flexible = jsl.fields.StringField()
        with jsl.roles.Scope(ROLE_v1_0_0) as v1:
            v1.not_so_user_friendly = jsl.fields.StringField(name="not so user-friendly")
        with jsl.roles.Scope(ROLE_v2_0_0) as v2:
            v2.not_so_user_friendly = jsl.fields.IntField(name="not so user-friendly")

    print(json.dumps(MyMultiformatDocument.get_schema(ordered=True, role=ROLE_v1_0_0), indent=2))
    return MyMultiformatDocument, ROLE_v2_0_0


@app.cell
def _(MyMultiformatDocument, ROLE_v2_0_0, json):
    print(json.dumps(MyMultiformatDocument.get_schema(ordered=True, role=ROLE_v2_0_0), indent=2))
    return


if __name__ == "__main__":
    app.run()
