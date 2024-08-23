import scrapy
from pathlib import Path


class LocationsSpider(scrapy.Spider):
    name = "locations"
    allowed_domains = ["traveltriangle.com"]
    start_urls = ["https://traveltriangle.com"]

    custom_settings = {
        'FEEDS': {
            'output/locations.csv': {
                'format': 'csv',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': ['name', 'image_link', 'description', 'best_time_to_visit', 'how_to_reach', 'places_to_visit', 'avg_temp'],
                'overwrite': True
            },
        }
    }

    def start_requests(self):
        urls = [
            "https://traveltriangle.com/blog/places-to-visit-in-india-before-you-turn-30/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = " ".join(response.url.split("/")[-2].split("-")[0:1])
        filename = f"locations-{page}.html"
        location_details = {}
        # Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
        
        places = response.css("h3")
        count = 0
        for place_temp in places:

            place = place_temp.attrib.get("id")

            name = place_temp.css("h3::text").get()
            #print(" ".join(name.split()[1:])) 
            
            image_link = response.xpath(f"//h3[@id='{place}']/following-sibling::div[1]/img/@data-src").get()
            #print(f"Image link for {place}: {image_link}")

            description = response.xpath(f"//h3[@id='{place}']/following-sibling::p[2]/text()").getall()
            print(f"Description for {place}: {description}")

            best_time = response.xpath(f"//h3[@id='{place}']/following-sibling::p[3]/text()").get()
            #print(f"Best time for {place}: {best_time}")

            
            how_to_reach_key = response.xpath(f"//h3[@id='{place}']/following-sibling::ul[1]//li/em/text()").getall()
            how_to_reach_values = response.xpath(f"//h3[@id='{place}']/following-sibling::ul[1]//li/text()[normalize-space()]").getall()

            if not how_to_reach_key:
                how_to_reach_key = response.xpath(f"//h3[@id='{place}']/following-sibling::p[position() < 6]/em/text()").getall()
                how_to_reach_values = response.xpath(f"//h3[@id='{place}']/following-sibling::p[position() < 6]/text()[normalize-space()]").getall()

            how_to_reach = {}
            for means, how_to_reach_value in zip(how_to_reach_key, how_to_reach_values):
                how_to_reach[means.strip(':')] = how_to_reach_value.strip()

            #print(f"How to reach {place}: {how_to_reach}")


            places_to_visit = response.xpath(f"//h3[@id='{place}']/following-sibling::p[position() <= 6][strong[contains(text(), 'Places to visit:') or contains(text(), 'Attractions:') or contains(text(), 'Things to do:') or contains(text(), 'Places To Visit:')]]/text()").getall()
            #print(f"Places to visit in {place}: {places_to_visit}")
            
            avg_temp = response.xpath(f"//h3[@id='{place}']/following-sibling::p[position() <= 7][strong[contains(text(), 'Average Temperature:') or contains(text(), 'Average Temperature') or contains(text(), ': ') or contains(text(), 'verage Temperature')]]/text()").get()       
            #print(f"Avg temp for {place}: {avg_temp}")

            count = count + 1

            # yield {
            #         'name': place,
            #         'image_link': image_link,
            #         'description': description,
            #         'best_time_to_visit': best_time,
            #         'how_to_reach': how_to_reach,
            #         'places_to_visit': places_to_visit,
            #         'avg_temp': avg_temp
            #     }

        print(count)
        
        
        
      
            