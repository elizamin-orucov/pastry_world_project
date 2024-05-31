class Uploader:

    @staticmethod
    def category_logo_uploader(instance, filename):
        return f"categories/{instance.name}/{filename}"

    @staticmethod
    def product_image_uploader(instance, filename):
        return f"products/{instance.product.name}/{filename}"

