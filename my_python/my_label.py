'''
Labeled_Image
'''
class Labeled_Image:
    #constructor
    def __init__(self, filepath, width, height, objects):
        self.filepath = filepath
        self.width    = width
        self.height   = height
        self.objects  = objects
    
'''
Labeled_Object
'''
class Labeled_Object:
    #constructor
    def __init__(self,class_id, class_name, x, y, width, height):
        self.class_id      = class_id
        self.class_name    = class_name
        self.x             = x
        self.y             = y
        self.width         = width
        self.height        = height
        self.visible_ratio = -1.0
        self.confidence    = -1.0
        self.iou           = -1.0
        self.object_id     = -1
        self.segmentation  = []
        
    '''
    It return a list of bbox's geometry.
    The geometries start from (0,0).
        [0] : top-left x of bounding-box
        [1] : top-left y of bounding-box
        [2] : bottom-right x of bounding-box
        [3] : bottom-right y of bounding-box    
    '''
    def get_rect(self):
        xmax = self.x + self.width
        ymax = self.y + self.height
        return [self.x, self.y, xmax, ymax]
    