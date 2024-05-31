from services.slugify import slugify

class Uploader:

    @staticmethod
    def category_logo_uploader(instance, filename):
        return f"categories/{slugify(instance.name)}/{filename}"

    @staticmethod
    def product_image_uploader(instance, filename):
        return f"products/{slugify(instance.product.name)}/{filename}"

    @staticmethod
    def blog_image_uploader(instance, filename):
        return f"blogs/{slugify(instance.blog.title)}/{filename}"

