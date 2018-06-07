
import os, sys, shutil
from xml.etree.ElementTree import *

class SkinFileConverter(object):
    """ This object provides methods to convert skin files from Default skin to all other skins
        It will replace font names and adjusts some more skin related attributes like radiobutton sizes etc.
        Required information is read from skin specific convert.xml files that reside in each skin folder
    """

    # base skin directory
    skin_path = os.path.join(os.path.dirname(__file__), 'resources', 'skins')
    # use skin files of Default skin as source for all other skins
    source_file_dir = os.path.join(skin_path, 'Default', '720p')

    def convert_skin_files(self):

        # get list of skins to convert
        skin_dirs = [d for d in os.listdir(self.skin_path) if os.path.isdir(os.path.join(self.skin_path, d))]

        for skin_dir in skin_dirs:
            if skin_dir != 'Default' and skin_dir != 'Confluence':
                target_dir = os.path.join(self.skin_path, skin_dir, '720p')
                skin_files = os.listdir(self.source_file_dir)
                convert_file = os.path.join(self.skin_path, skin_dir, 'convert.xml')
                if not os.path.exists(convert_file):
                    print 'convert file does not exist: %s' %convert_file
                    continue
                for skin_file in skin_files:
                    source_file = os.path.join(self.source_file_dir, skin_file)
                    target_file = os.path.join(target_dir, skin_file)

                    self.convert_skin_file(source_file, target_file, convert_file)

    def convert_skin_file(self, source_file, target_file, convert_file):
        tree = ElementTree()
        if sys.version_info >= (2, 7):
            parser = XMLParser(encoding='utf-8')
        else:
            parser = XMLParser()

        tree.parse(convert_file, parser)
        fonts = tree.findall('fonts/font')

        with open(source_file, "rt") as fin:
            with open(target_file, "wt") as fout:
                for line in fin:
                    for font in fonts:
                        # font looks like this in convert.xml:
                        # <font name="font10">Mini</font>
                        # Estuary font names as attribute name, new skin font names as element text
                        line = line.replace(font.attrib.get('name'), font.text)
                    fout.write(line)



