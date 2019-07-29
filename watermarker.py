# Created by Dare McAdewole <dare.dev.adewole@gmail.com>
from PIL import Image, ImageFilter, ImageColor
from pathlib import Path

class Watermarker:
    """Watermarker
    
    Raises:
        Exception: [description]
    
    Returns:
        [type] -- [description]
    """
    __gap__ = 20

    @staticmethod
    def set_gap(gap):
        Watermarker.__gap__ = gap

    @staticmethod
    def watermark(path_to_image, watermark_image, destination_image, position=None):
        """Watermark Image

        Arguments:
            path_to_image {str} -- Path to the image to be watermarked
            position {str} -- Defines where the watermarked image should go
        """
        source_image_props = dict(
            width=None,
            height=None,
            format=None
        )
        formats = ( 'png', 'jpg' )
        destination_image_format = destination_image[len(destination_image) - 3:].lower()
        # If position is not provided, set the default position
        if position == None:
            position = Watermarker.Position.bottom_right
        if destination_image_format != 'png':
            raise WatermarkerError.InvalidFormat
        watermark = None
        try:
            # Open main image
            with Image.open(path_to_image) as source_image:
                # get image properties
                source_image_props['width'] = source_image.size[0]
                source_image_props['height'] = source_image.size[1]
                source_image_props['format'] = source_image.format
                with Image.open(watermark_image).convert('LA') as watermark_file:
                    image_width = watermark_file.size[0]
                    image_height = watermark_file.size[1]
                    box = (0, 0, image_width, image_height)
                    watermark = watermark_file.crop(box)
                    source_image.paste(
                        watermark,
                        Watermarker.__getposition__(
                            position,
                            source_image_props['width'],
                            source_image_props['height'],
                            image_width,
                            image_height
                        )
                    )
                    source_image.save(destination_image)
        except FileNotFoundError:
            raise WatermarkerError.SourceFileNotFound
        except IOError:
            raise WatermarkerError.IO

        position_maps = []
        return source_image

    @staticmethod
    def __getposition__ (pos, miw, mih, wiw, wih):
        """Gets appropriate position of watermark from string
        
        Arguments:
            pos {Watermarker.Position} -- The position of the watermark
            miw {int} -- Main Image width
            mih {int} -- Main Image Height
            wiw {int} -- Watermark Image width
            wih {int} -- Watermark Image height
        
        Returns:
            [type] -- [description]
        """
        gap = Watermarker.__gap__
        position = None
        if pos == Watermarker.Position.top_left:
            position = (gap, gap)
        elif pos == Watermarker.Position.top_center:
            position = (int((miw/2) - (wiw/2)), gap)
        elif pos == Watermarker.Position.top_right:
            position = (miw - (gap + wiw), gap)
        elif pos == Watermarker.Position.bottom_left:
            position = (gap, mih - (gap + wih))
        elif pos == Watermarker.Position.bottom_center:
            position = (int((miw/2) - (wiw/2)), mih - (gap + wih))
        elif pos == Watermarker.Position.bottom_right:
            position = (miw - (gap + wiw), mih - (gap + wih))
        elif pos == Watermarker.Position.center:
            position = (int((miw/2) - (wiw/2)), int((mih/2) - (wih/2)))
        return position

    class Position:
        # Top Positions
        top_left = 0
        top_center = 1
        top_right = 2

        # Bottom positions
        bottom_left = 3
        bottom_center = 4
        bottom_right = 5

        center = 6


# Exceptions
class WatermarkerError:
    class InvalidFormat (Exception):
        """ Raised when the format of the image argument is Invalid """
        pass

    class SourceFileNotFound (Exception):
        """Raised when Source File is not found"""
        pass

    class IO (Exception):
        """Raised when Source File is not found"""
        pass
