from django.db import models
# You'll need to Install & Import Pillow to use Images in Django
from PIL import Image


# for example, we'll have a company with only a name & a logo
class Company(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name='Company Name',
    )
    logo = models.ImageField(
        default='default.jpg',
        upload_to='company_logos',
        verbose_name='Company Logo',
    )

    # to crop the image we define a custom save method, so everytime .save() is called our code runs
    # this code is made to output an image with a 1:1 ratio 
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # the desired output resolution
        output_resolution = 600
        # set it to the default image size, to avoid cropping the default image (in case it has a different resolution)
        # it also won't change the size of any image that has the same w and h
        # if you want it to be specific to the default image you can check with both the resolution and name
        default_size = 512
        if self.logo:
            image = Image.open(self.logo.path)
            w, h = image.size
            # if the width and height does not match the default image we proceed
            # otherwise we do nothing 
            if h != default_size or w != default_size:
                # if the height or width is smaller than the output_resolution, we set the output_resolution to the minimum of the smaller one 
                if h < output_resolution or w < output_resolution:
                    if w > h:
                        output_resolution = h
                    else:
                        output_resolution = w
                # if the image is already has a 1:1 ratio we just need to resize it 
                if w == h:
                    image = image.resize((output_resolution, output_resolution))
                    image.save(self.logo.path)
                # if the image is horizontal we'll need to crop it from the left and the right
                elif w > h:
                    left = (w - h)/2        # since we're cropping from left & right (for the image to be centered)
                    top = 0
                    right = (w + h)/2       # we'll crop half the difference from the left and the other half from the right
                    bottom = h
                    # first we crop the image
                    image = image.crop((left, top, right, bottom))
                    # we only resize the image after cropping it
                    image = image.resize((output_resolution, output_resolution))
                    image.save(self.logo.path)
                # if the image is vertical we'll need to crop it from the left and the right
                else:
                    left = 0
                    top = (h - w)/2         # since we're cropping from top & bottom (for the image to be centered)
                    right = w
                    bottom = (h + w)/2      # we'll crop half the difference from the top and the other half from the bottom
                    # first we crop the image
                    image = image.crop((left, top, right, bottom))
                    # we only resize the image after cropping it
                    image = image.resize((output_resolution, output_resolution))
                    image.save(self.logo.path)