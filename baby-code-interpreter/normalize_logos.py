from PIL import Image


def resize_images(image_paths, new_dimensions):
    for image_path in image_paths:
        img = Image.open(image_path)
        img = img.resize(new_dimensions)
        img.save(image_path)


# image paths
image_paths = ["./assets/footer/html_css_js.png",
               "./assets/footer/langchain.png",
               "./assets/footer/llama_cpp.png",
               "./assets/footer/meta_llama_2.png",
               "./assets/footer/python.png"]

# nice friendly dimensions for the carousel icons.
new_dimensions = (691, 361)

resize_images(image_paths, new_dimensions)
