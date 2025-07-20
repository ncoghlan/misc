import marimo

__generated_with = "0.14.12"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Digital Blasphemy Wallpaper Sync
    ================================

    [Digital Blasphemy](http://digitalblasphemy.com) is a great site where the digital artist Ryan Bliss posts a wide variety of wallpapers for download.

    While a selection of the pieces are available for free, subscribing to the site provides access to all of the images at a variety of resolutions. Given how much I like Ryan's art, I signed up for a lifetime subscription to help ensure I'll have more artwork to download in the future :)

    I've long used a random selection of the Digital Blasphemy artwork as the desktop background on my personal laptop, but for a long time updating the available images was a matter of downloading the complete zip archives at the relevant resolutions, unzipping them to the appropriate location, and then going through them to delete the few that I know I don't like (or don't mind myself, but wouldn't be happy to have on-screen at a professional conference).

    Eventually, I decided to solve the problem in a more sensible way, by figuring out a way to automate the process of checking for images I didn't have (in the resolutions I care about) and downloading them to the right location.

    Packaging that up properly as a command line application would be a lot of work that wouldn't really help *me*, but by using an IPython notebook, I was able to convert my experimental code to see how I could retrieve the relevant data from the site directly into something that actually solved my original problem :)

    That selective download solution eventually broke when the website migrated from a simple basic auth protected file server to a full CDN, so the notebook was rewritten in Marimo to work from the per-resolution archive downloads.

    If the name Digital Blasphemy sounds vaguely familiar, it may be due to *this* image (or one of its earlier incarnations):

    ![Flourescence (2009 version)](https://cdn.digitalblasphemy.com/thumbnail/980x735/fluorescence2k93_thumbnail_980x735.jpg)

    Using the notebook
    --------------------

    1. Save an up to date https://digitalblasphemy.com/zip-files/ archive to your local image folder
    2. Load the notebook using marimo (the only dependency is the standard library)
    3. Ensure the local image folder is listed under `CANDIDATE_IMAGE_DIRS`
    4. Ensure the `RESOLUTIONS` list covers the image resolutions to be unpacked
    5. Optionally, update the `EXCLUDED` global to nominate particular images you don't want to unpack
    6. Run the whole notebook - the checked in version does a dry run by default
    7. If the dry run output looks sensible, change DRY_RUN to False and run the notebook again
    """
    )
    return


@app.cell
def _():
    import zipfile
    from pathlib import Path

    # Default file paths are set up for my personal WSL and native Linux setups
    # Currently assumes the use of single-screen DB images

    DRY_RUN = True
    PERMISSIVE_FILTER = True
    CANDIDATE_IMAGE_DIRS = [
        Path("~/Pictures/Digital Blasphemy/").expanduser(),
        Path("/mnt/e/Digital Blasphemy/")

    ]
    for LOCAL_IMAGE_DIR in CANDIDATE_IMAGE_DIRS:
        if LOCAL_IMAGE_DIR.exists():
            break
    else:
        raise RuntimeError("Failed to open local image folder")
    RESOLUTIONS = ["2560x1440"]
    def resolution_archive_path(resolution):
        return LOCAL_IMAGE_DIR / f"single_{resolution}.zip"
    def relative_resolution_dir(resolution):
        return f"digitalblasphemy/wallpapers/single/{resolution}/"
    def resolution_folder_path(resolution):
        return LOCAL_IMAGE_DIR / f"single_{resolution}" / relative_resolution_dir(resolution)
    IMAGE_ARCHIVE_PATHS = {res: resolution_archive_path(res) for res in RESOLUTIONS}
    ARCHIVE_RES_DIRS = {res: relative_resolution_dir(res) for res in RESOLUTIONS}
    EXTRACTED_RES_DIRS = {res: resolution_folder_path(res) for res in RESOLUTIONS}
    return (
        ARCHIVE_RES_DIRS,
        DRY_RUN,
        EXTRACTED_RES_DIRS,
        IMAGE_ARCHIVE_PATHS,
        LOCAL_IMAGE_DIR,
        PERMISSIVE_FILTER,
        RESOLUTIONS,
        zipfile,
    )


@app.cell
def _(PERMISSIVE_FILTER):
    # I use my laptop for conference presentations
    # If I either don't really like a wallpaper or I'm
    # not happy displaying it at a professional
    # conference, I ensure I don't extract it
    ALWAYS_OMIT = ("cupid", "emblem", "taketwo")
    if PERMISSIVE_FILTER:
        EXCLUDED = ALWAYS_OMIT
    else:
        # Fine for personal use, risks complaints at a conference
        EXCLUDED = ("chamelea", *ALWAYS_OMIT)
    return (EXCLUDED,)


@app.cell
def _(EXCLUDED):
    def iter_archive_image_entries(image_res_zpath):
        if not image_res_zpath.exists():
            raise Exception(f"{image_res_zpath} is not in the archive")
        if not image_res_zpath.is_dir():
            raise Exception(f"{image_res_zpath} is not an archive folder")
        for zpath in image_res_zpath.iterdir():
            candidate = zpath.name
            if not candidate.startswith(EXCLUDED):
                yield candidate

    def get_archive_image_names(image_res_zpath):
        return set(iter_archive_image_entries(image_res_zpath))

    def get_local_image_names(local_path):
        return set(p.name for p in local_path.iterdir())
    return get_archive_image_names, get_local_image_names


@app.cell
def _(
    ARCHIVE_RES_DIRS,
    EXTRACTED_RES_DIRS,
    IMAGE_ARCHIVE_PATHS,
    LOCAL_IMAGE_DIR,
    get_archive_image_names,
    get_local_image_names,
    zipfile,
):
    import time

    def get_images_to_extract(archive_image_zpath, dest_dir_path):
        archive_image_names = get_archive_image_names(archive_image_zpath)
        local_image_names = get_local_image_names(dest_dir_path)
        return archive_image_names - local_image_names

    def extract_image(source_zpath: zipfile.Path, dry_run=True):
        zf = source_zpath.root
        extract_root = (LOCAL_IMAGE_DIR / zf.filename).with_suffix("")
        dest_path = extract_root / source_zpath.at
        print(f"  Extracting {source_zpath} -> {dest_path}")
        if dry_run:
            print("    Dry run only, skipping extraction")
        else:
            zf.extract(source_zpath.at, extract_root)
        return dest_path


    # This assumes the local destination directory already exists
    def extract_missing_images_for_res(resolution, dry_run=True):
        archive_path = IMAGE_ARCHIVE_PATHS[resolution]
        archive_image_dir = ARCHIVE_RES_DIRS[resolution]
        dest_dir_path = EXTRACTED_RES_DIRS[resolution]
        delay = 0.05
        image_archive = zipfile.ZipFile(archive_path)
        archive_image_zpath = zipfile.Path(image_archive, archive_image_dir)
        image_names = get_images_to_extract(archive_image_zpath, dest_dir_path)
        total = len(image_names)
        if not total:
            print("No {} images to extract".format(resolution))
            return
        print("{} {} images to be extracted".format(total, resolution))
        extracted_images = []
        for i, image in enumerate(image_names, start=1):
            print("Extracting {} image {}/{}".format(resolution, i, total))
            source_zpath = archive_image_zpath / image
            dest_path = extract_image(source_zpath, dry_run)
            extracted_images.append(dest_path)
            time.sleep(delay) # Be nice to the server
        return extracted_images

    def extract_missing_images(dry_run=True):
        updated_resolutions = {}
        for res in IMAGE_ARCHIVE_PATHS.keys():
            images = extract_missing_images_for_res(res, dry_run)
            if images:
                updated_resolutions[res] = images
        return updated_resolutions
    return (extract_missing_images,)


@app.cell
def _(mo):
    # TODO: Show images directly from archive in dry_run mode
    def show_images(filenames):
        for filename in filenames:
            mo.output.append(mo.image(src=filename))
    return (show_images,)


@app.cell
def _(DRY_RUN, extract_missing_images):
    extracted = extract_missing_images(dry_run=DRY_RUN)
    return (extracted,)


@app.cell
def _(DRY_RUN, RESOLUTIONS, extracted, show_images):
    if extracted and not DRY_RUN:
        show_images(extracted[RESOLUTIONS[0]])
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
