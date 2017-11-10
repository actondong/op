from BeautifulSoup import BeautifulSoup
from urllib import urlretrieve
import sys,os
from selenium import webdriver
import glob
import time
from PIL import Image

class op_episode_generator:

    def __init__(self):
        #self.html = codecs.open(html_file, 'r')
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(180)  # seconds

    def get_episode(self, url):

        # use firefox to get page with javascript generated content
        self.driver.get(url)
        page = self.driver.page_source
        return page

    def create_episode(self, url, episode):

        page_src = self.get_episode(url)
        parsed_html = BeautifulSoup(page_src)
        episode_content = None
        while episode_content is None:
            try:
                episode_content = parsed_html.find('div',{'class':'post-img'})
            except:
                time.sleep(10)

        content = episode_content.findAll('img')
        num = 1
        list_im = []
        num_tries = 0
        while num < len(content):

            if num_tries > 2*len(content):
                print "Error--->" + str(episode)
                break

            image = content[num]
            num_tries +=1

            try:

                if image.has_key("data-src"):
                    img_url = 'http:' + image["data-src"].lower()
                else:
                    img_url = 'http:' + image["src"].lower()

                fn = "pic" + str(num) + ".png"
                urlretrieve(img_url, fn)

            except:
                continue

            list_im.append(fn)
            num += 1

        images = map(Image.open, list_im)
        widths, heights = zip(*(i.size for i in images))

        max_width = max(widths)
        total_height = sum(heights)

        new_im = Image.new('RGB', (max_width, total_height))

        x_offset = 0
        for im in images:
            new_im.paste(im, (0, x_offset))
            x_offset += im.size[1]

        new_im.save(str(episode)+'.png')

        for f in glob.glob("pic*.png"):
            os.remove(f)


def main():

    # urls = ["http://hanhuazu.cc/cartoon/post?id=8947","http://hanhuazu.cc/cartoon/post?id=8926","http://hanhuazu.cc/cartoon/post?id=8906","http://hanhuazu.cc/cartoon/post?id=8882","http://hanhuazu.cc/cartoon/post?id=8837","http://hanhuazu.cc/cartoon/post?id=8795","http://hanhuazu.cc/cartoon/post?id=8764","http://hanhuazu.cc/cartoon/post?id=8736","http://hanhuazu.cc/cartoon/post?id=8676","http://hanhuazu.cc/cartoon/post?id=8659"]
    # episode = 869
    url = sys.argv[1]
    episode = sys.argv[2]

    episode_generator = op_episode_generator()
    episode_generator.create_episode(url,episode)


if __name__ == "__main__":
    main()