from lib.exceptions    import DuplicateDocument
from lib.model.post    import Post
from lib.factory.saver import SaverFactory
from grab.spider       import Spider, Task
from selection         import XpathSelector
import multiprocessing
import arrow

class KaskusSpider(Spider):
	def task_generator(self):
		self.saver, 		      = self.args
		self.crawler_name         = "Kaskus Crawler"
		self.country 			  = "IDN"
		self.thread_link_xpath    = "//a[re:test(@id,'thread_title_')]"
		self.last_page_xpath      = "//ul[@class='pagination']/li[last()]//a"
		self.post_xpath           = "//div[re:test(@id,'post[0-9]')]"
		self.permalink_xpath      = ".//div[@class='permalink']/a"
		self.published_date_xpath = ".//time[@class='entry-date']"
		self.title_xpath 		  = "//div[@class='current']"
		self.content_xpath        = ".//div[@class='entry']"
		self.author_name_xpath    = ".//div[@class='user-name']//span[@itemprop='name']"
		self.categories 	      = [
			"http://www.kaskus.co.id/forum/570/kendaraan-roda-4",
			"http://www.kaskus.co.id/forum/34/all-about-design",
			"http://www.kaskus.co.id/forum/671/animasi",
			"http://www.kaskus.co.id/forum/655/komik--ilustrasi",
			"http://www.kaskus.co.id/forum/26/anime--manga-haven",
			"http://www.kaskus.co.id/forum/116/amhelpdesk",
			"http://www.kaskus.co.id/forum/431/anime",
			"http://www.kaskus.co.id/forum/552/fanstuff",
			"http://www.kaskus.co.id/forum/433/manga-manhua-amp-manhwa",
			"http://www.kaskus.co.id/forum/390/tokusenka",
			"http://www.kaskus.co.id/forum/122/western-comic",
			"http://www.kaskus.co.id/forum/244/latest-release",
			"http://www.kaskus.co.id/forum/83/canada",
			"http://www.kaskus.co.id/forum/421/visit-usa",
			"http://www.kaskus.co.id/forum/425/central-usa",
			"http://www.kaskus.co.id/forum/96/east-usa",
			"http://www.kaskus.co.id/forum/423/west-usa",
			"http://www.kaskus.co.id/forum/115/china",
			"http://www.kaskus.co.id/forum/108/japan",
			"http://www.kaskus.co.id/forum/77/singapore",
			"http://www.kaskus.co.id/forum/477/others",
			"http://www.kaskus.co.id/forum/540/korea-selatan",
			"http://www.kaskus.co.id/forum/90/malaysia",
			"http://www.kaskus.co.id/forum/384/brisbane",
			"http://www.kaskus.co.id/forum/79/melbourne",
			"http://www.kaskus.co.id/forum/106/perth",
			"http://www.kaskus.co.id/forum/80/sydney",
			"http://www.kaskus.co.id/forum/475/others",
			"http://www.kaskus.co.id/forum/10/berita-dan-politik",
			"http://www.kaskus.co.id/forum/732/berita-dunia-hiburan",
			"http://www.kaskus.co.id/forum/746/beritagarid",
			"http://www.kaskus.co.id/forum/250/berita-luar-negeri",
			"http://www.kaskus.co.id/forum/731/berita-olahraga",
			"http://www.kaskus.co.id/forum/733/citizen-journalism",
			"http://www.kaskus.co.id/forum/730/metrotvnewscom",
			"http://www.kaskus.co.id/forum/30/bisnis",
			"http://www.kaskus.co.id/forum/546/dunia-kerja--profesi",
			"http://www.kaskus.co.id/forum/277/entrepreneur-corner",
			"http://www.kaskus.co.id/forum/466/penawaran-kerjasama--investasi",
			"http://www.kaskus.co.id/forum/279/forex-option-saham--derivatifnya",
			"http://www.kaskus.co.id/forum/467/forex",
			"http://www.kaskus.co.id/forum/470/forex-broker",
			"http://www.kaskus.co.id/forum/469/saham",
			"http://www.kaskus.co.id/forum/468/options",
			"http://www.kaskus.co.id/forum/278/lowongan-kerja",
			"http://www.kaskus.co.id/forum/472/mlm-member-get-member--sejenisnya",
			"http://www.kaskus.co.id/forum/572/penawaran-kerjasama-bo-distribusi-reseller--agen",
			"http://www.kaskus.co.id/forum/737/reksa-dana",
			"http://www.kaskus.co.id/forum/571/the-exclusive-business-club-exbc",
			"http://www.kaskus.co.id/forum/471/the-online-business",
			"http://www.kaskus.co.id/forum/280/hyip---money-game---ptc---autosurf",
			"http://www.kaskus.co.id/forum/595/ukm",
			"http://www.kaskus.co.id/forum/66/buku",
			"http://www.kaskus.co.id/forum/18/can-you-solve-this-game",
			"http://www.kaskus.co.id/forum/19/computer-stuff",
			"http://www.kaskus.co.id/forum/243/hardware-computer",
			"http://www.kaskus.co.id/forum/183/internet-service-amp-networking",
			"http://www.kaskus.co.id/forum/65/linux-dan-os-selain-microsoft-amp-mac",
			"http://www.kaskus.co.id/forum/383/macintosh",
			"http://www.kaskus.co.id/forum/176/programmer-forum",
			"http://www.kaskus.co.id/forum/13/website-webmaster-webdeveloper",
			"http://www.kaskus.co.id/forum/557/hardware-review-lab",
			"http://www.kaskus.co.id/forum/397/isp",
			"http://www.kaskus.co.id/forum/569/mac-applications-amp-games",
			"http://www.kaskus.co.id/forum/568/mac-osx-info-amp-discussion",
			"http://www.kaskus.co.id/forum/443/hosting-stuff",
			"http://www.kaskus.co.id/forum/442/templates-amp-scripts-stuff",
			"http://www.kaskus.co.id/forum/29/cooking--resto-guide",
			"http://www.kaskus.co.id/forum/62/oriental-exotic-asian-food",
			"http://www.kaskus.co.id/forum/248/restaurant-review",
			"http://www.kaskus.co.id/forum/60/selera-nusantara-indonesian-food",
			"http://www.kaskus.co.id/forum/63/the-kaskus-bar",
			"http://www.kaskus.co.id/forum/61/the-rest-of-the-world-international-food",
			"http://www.kaskus.co.id/forum/713/deals",
			"http://www.kaskus.co.id/forum/191/debate-club",
			"http://www.kaskus.co.id/forum/15/disturbing-picture",
			"http://www.kaskus.co.id/forum/67/education",
			"http://www.kaskus.co.id/forum/281/electronics",
			"http://www.kaskus.co.id/forum/113/english",
			"http://www.kaskus.co.id/forum/474/event-from-kaskuser",
			"http://www.kaskus.co.id/forum/247/civitas-academica",
			"http://www.kaskus.co.id/forum/246/sejarah-amp-xenology",
			"http://www.kaskus.co.id/forum/597/sains--teknologi",
			"http://www.kaskus.co.id/forum/282/audio-amp-video",
			"http://www.kaskus.co.id/forum/673/home-appliance",
			"http://www.kaskus.co.id/forum/464/english-education-amp-literature",
			"http://www.kaskus.co.id/forum/465/fun-with-english",
			"http://www.kaskus.co.id/forum/82/germany",
			"http://www.kaskus.co.id/forum/85/netherlands",
			"http://www.kaskus.co.id/forum/129/united-kingdom",
			"http://www.kaskus.co.id/forum/476/others",
			"http://www.kaskus.co.id/forum/44/games",
			"http://www.kaskus.co.id/forum/678/gemstone",
			"http://www.kaskus.co.id/forum/39/girls--boyss-corner",
			"http://www.kaskus.co.id/forum/630/green-lifestyle",
			"http://www.kaskus.co.id/forum/720/game-news-and-events",
			"http://www.kaskus.co.id/forum/119/console-amp-handheld-games",
			"http://www.kaskus.co.id/forum/100/online-games",
			"http://www.kaskus.co.id/forum/528/pc-games",
			"http://www.kaskus.co.id/forum/38/web-based-games",
			"http://www.kaskus.co.id/forum/114/ask-da-boys",
			"http://www.kaskus.co.id/forum/105/ask-da-girls",
			"http://www.kaskus.co.id/forum/721/mobile-games",
			"http://www.kaskus.co.id/forum/722/arcade-games",
			"http://www.kaskus.co.id/forum/711/dota-2",
			"http://www.kaskus.co.id/forum/710/moba",
			"http://www.kaskus.co.id/forum/709/private-servers",
			"http://www.kaskus.co.id/forum/37/ragnarok-online",
			"http://www.kaskus.co.id/forum/36/handphone--tablet",
			"http://www.kaskus.co.id/forum/94/health",
			"http://www.kaskus.co.id/forum/16/heart-to-heart",
			"http://www.kaskus.co.id/forum/32/hewan-peliharaan",
			"http://www.kaskus.co.id/forum/392/hobby--community",
			"http://www.kaskus.co.id/forum/577/android",
			"http://www.kaskus.co.id/forum/307/blackberry-corner",
			"http://www.kaskus.co.id/forum/672/ios",
			"http://www.kaskus.co.id/forum/413/featured-phone",
			"http://www.kaskus.co.id/forum/417/operator-cdma--gsm",
			"http://www.kaskus.co.id/forum/541/windows-phone",
			"http://www.kaskus.co.id/forum/558/fitness--healthy-body",
			"http://www.kaskus.co.id/forum/49/b-log-collections",
			"http://www.kaskus.co.id/forum/50/poetry",
			"http://www.kaskus.co.id/forum/51/stories-from-the-heart",
			"http://www.kaskus.co.id/forum/124/burung",
			"http://www.kaskus.co.id/forum/127/freshwater-fish",
			"http://www.kaskus.co.id/forum/123/mamalia",
			"http://www.kaskus.co.id/forum/125/reptil",
			"http://www.kaskus.co.id/forum/126/saltwater-fish",
			"http://www.kaskus.co.id/forum/591/jam",
			"http://www.kaskus.co.id/forum/581/lampu-senter---flashlight",
			"http://www.kaskus.co.id/forum/395/mancing",
			"http://www.kaskus.co.id/forum/393/pisau",
			"http://www.kaskus.co.id/forum/580/radio-komunikasi",
			"http://www.kaskus.co.id/forum/394/sepeda",
			"http://www.kaskus.co.id/forum/674/vaporizer",
			"http://www.kaskus.co.id/forum/274/fat-lossgain-massnutrisi-diet--suplementasi-fitness",
			"http://www.kaskus.co.id/forum/236/muscle-building",
			"http://www.kaskus.co.id/forum/724/health-consultation",
			"http://www.kaskus.co.id/forum/725/healthy-lifestyle",
			"http://www.kaskus.co.id/forum/559/quit-smoking-alcohol--drugs",
			"http://www.kaskus.co.id/forum/735/b-log-community",
			"http://www.kaskus.co.id/forum/734/b-log-personal",
			"http://www.kaskus.co.id/forum/387/ilmu-marketing",
			"http://www.kaskus.co.id/forum/427/papua",
			"http://www.kaskus.co.id/forum/89/bandung",
			"http://www.kaskus.co.id/forum/164/banten",
			"http://www.kaskus.co.id/forum/405/bekasi",
			"http://www.kaskus.co.id/forum/107/bogor",
			"http://www.kaskus.co.id/forum/412/cirebon",
			"http://www.kaskus.co.id/forum/407/depok",
			"http://www.kaskus.co.id/forum/654/garut",
			"http://www.kaskus.co.id/forum/78/dki-jakarta",
			"http://www.kaskus.co.id/forum/626/karawang",
			"http://www.kaskus.co.id/forum/585/sukabumi",
			"http://www.kaskus.co.id/forum/599/tasikmalaya",
			"http://www.kaskus.co.id/forum/181/banyumas",
			"http://www.kaskus.co.id/forum/653/cilacap",
			"http://www.kaskus.co.id/forum/627/karesidenan-kedu",
			"http://www.kaskus.co.id/forum/564/karesidenan-pati",
			"http://www.kaskus.co.id/forum/598/klaten",
			"http://www.kaskus.co.id/forum/111/semarang",
			"http://www.kaskus.co.id/forum/160/solo",
			"http://www.kaskus.co.id/forum/402/tegal",
			"http://www.kaskus.co.id/forum/84/yogyakarta",
			"http://www.kaskus.co.id/forum/583/mojokerto",
			"http://www.kaskus.co.id/forum/628/sidoarjo",
			"http://www.kaskus.co.id/forum/92/surabaya",
			"http://www.kaskus.co.id/forum/133/malang",
			"http://www.kaskus.co.id/forum/167/bali",
			"http://www.kaskus.co.id/forum/587/bromo",
			"http://www.kaskus.co.id/forum/567/gresik",
			"http://www.kaskus.co.id/forum/555/jember",
			"http://www.kaskus.co.id/forum/403/karesidenan-besuki",
			"http://www.kaskus.co.id/forum/651/karesidenan-bojonegoro",
			"http://www.kaskus.co.id/forum/452/karesidenan-kediri",
			"http://www.kaskus.co.id/forum/411/karesidenan-madiun",
			"http://www.kaskus.co.id/forum/652/madura",
			"http://www.kaskus.co.id/forum/162/kalimantan-barat",
			"http://www.kaskus.co.id/forum/146/kalimantan-selatan",
			"http://www.kaskus.co.id/forum/385/kalimantan-tengah",
			"http://www.kaskus.co.id/forum/91/kalimantan-timur---kalimantan-utara",
			"http://www.kaskus.co.id/forum/584/gorontalo",
			"http://www.kaskus.co.id/forum/561/kendari",
			"http://www.kaskus.co.id/forum/170/makassar",
			"http://www.kaskus.co.id/forum/179/manado",
			"http://www.kaskus.co.id/forum/166/palu",
			"http://www.kaskus.co.id/forum/161/aceh",
			"http://www.kaskus.co.id/forum/117/riau-raya",
			"http://www.kaskus.co.id/forum/97/bangka---belitung",
			"http://www.kaskus.co.id/forum/543/batam",
			"http://www.kaskus.co.id/forum/586/bengkulu",
			"http://www.kaskus.co.id/forum/548/jambi",
			"http://www.kaskus.co.id/forum/398/kepulauan-riau",
			"http://www.kaskus.co.id/forum/145/lampung",
			"http://www.kaskus.co.id/forum/93/medan",
			"http://www.kaskus.co.id/forum/156/minangkabau",
			"http://www.kaskus.co.id/forum/81/palembang",
			"http://www.kaskus.co.id/forum/9/jokes--cartoon",
			"http://www.kaskus.co.id/forum/331/pictures",
			"http://www.kaskus.co.id/forum/689/stand-up-comedy",
			"http://www.kaskus.co.id/forum/629/kaskus-playground",
			"http://www.kaskus.co.id/forum/240/kaskus-peduli",
			"http://www.kaskus.co.id/forum/263/kaskus-celeb",
			"http://www.kaskus.co.id/forum/435/kaskus-promo",
			"http://www.kaskus.co.id/forum/479/cinta-indonesiaku",
			"http://www.kaskus.co.id/forum/480/arsitektur",
			"http://www.kaskus.co.id/forum/485/kekayaan-alam-flora--fauna",
			"http://www.kaskus.co.id/forum/481/kuliner",
			"http://www.kaskus.co.id/forum/484/kerajinan--ukiran",
			"http://www.kaskus.co.id/forum/486/kesusastraan-bahasa--dongeng",
			"http://www.kaskus.co.id/forum/482/pakaian",
			"http://www.kaskus.co.id/forum/483/lagu-tarian--alat-musik",
			"http://www.kaskus.co.id/forum/542/pahlawan--tokoh-nasional",
			"http://www.kaskus.co.id/forum/488/permainan-rakyat",
			"http://www.kaskus.co.id/forum/490/properti-sejarah-nasional",
			"http://www.kaskus.co.id/forum/489/seni-peran",
			"http://www.kaskus.co.id/forum/487/tata-cara-adat-upacara--ritual",
			"http://www.kaskus.co.id/forum/473/gathering-event-report--bakti-sosial",
			"http://www.kaskus.co.id/forum/675/ngampus-di-kaskus",
			"http://www.kaskus.co.id/forum/663/jual-beli-zone",
			"http://www.kaskus.co.id/forum/273/product-review",
			"http://www.kaskus.co.id/forum/594/melek-hukum",
			"http://www.kaskus.co.id/forum/575/militer-dan-kepolisian",
			"http://www.kaskus.co.id/forum/491/mobile-broadband",
			"http://www.kaskus.co.id/forum/70/model-kit--r-c",
			"http://www.kaskus.co.id/forum/11/movies",
			"http://www.kaskus.co.id/forum/33/music",
			"http://www.kaskus.co.id/forum/576/kepolisian",
			"http://www.kaskus.co.id/forum/87/music-review",
			"http://www.kaskus.co.id/forum/140/militer",
			"http://www.kaskus.co.id/forum/252/figures",
			"http://www.kaskus.co.id/forum/253/gallery-amp-tutorial",
			"http://www.kaskus.co.id/forum/251/plamo",
			"http://www.kaskus.co.id/forum/621/film-indonesia",
			"http://www.kaskus.co.id/forum/619/indie-filmmaker",
			"http://www.kaskus.co.id/forum/736/series--film-asia",
			"http://www.kaskus.co.id/forum/88/help-tips-amp-tutorial",
			"http://www.kaskus.co.id/forum/58/kaskusradiocom",
			"http://www.kaskus.co.id/forum/386/music-event",
			"http://www.kaskus.co.id/forum/98/outdoor-adventure--nature-clubs",
			"http://www.kaskus.co.id/forum/596/catatan-perjalanan-oanc",
			"http://www.kaskus.co.id/forum/620/perencanaan-keuangan",
			"http://www.kaskus.co.id/forum/54/photography",
			"http://www.kaskus.co.id/forum/712/pilkada",
			"http://www.kaskus.co.id/forum/194/timur-tengah",
			"http://www.kaskus.co.id/forum/478/others",
			"http://www.kaskus.co.id/forum/715/sista",
			"http://www.kaskus.co.id/forum/35/sports",
			"http://www.kaskus.co.id/forum/668/suara-kaskusers",
			"http://www.kaskus.co.id/forum/23/supranatural",
			"http://www.kaskus.co.id/forum/188/surat-pembaca",
			"http://www.kaskus.co.id/forum/717/beauty",
			"http://www.kaskus.co.id/forum/716/fashionista",
			"http://www.kaskus.co.id/forum/718/womens-health",
			"http://www.kaskus.co.id/forum/187/airsoft-indonesia",
			"http://www.kaskus.co.id/forum/440/basketball",
			"http://www.kaskus.co.id/forum/276/grappling",
			"http://www.kaskus.co.id/forum/723",
			"http://www.kaskus.co.id/forum/332/racing---balap",
			"http://www.kaskus.co.id/forum/144/martial-arts",
			"http://www.kaskus.co.id/forum/545/pro-wrestling",
			"http://www.kaskus.co.id/forum/538/racket",
			"http://www.kaskus.co.id/forum/104/soccer-amp-futsal-room",
			"http://www.kaskus.co.id/forum/685/f1",
			"http://www.kaskus.co.id/forum/684/motogp",
			"http://www.kaskus.co.id/forum/539/badminton",
			"http://www.kaskus.co.id/forum/565/futsal",
			"http://www.kaskus.co.id/forum/661/sundul-eropa",
			"http://www.kaskus.co.id/forum/537/sport-games",
			"http://www.kaskus.co.id/forum/192/tanaman",
			"http://www.kaskus.co.id/forum/578/teknik",
			"http://www.kaskus.co.id/forum/21/the-lounge",
			"http://www.kaskus.co.id/forum/235/travellers",
			"http://www.kaskus.co.id/forum/234/arsitektur",
			"http://www.kaskus.co.id/forum/579/sipil",
			"http://www.kaskus.co.id/forum/713",
			"http://www.kaskus.co.id/forum/59/gosip-nyok",
			"http://www.kaskus.co.id/forum/708/indonesia-pusaka",
			"http://www.kaskus.co.id/forum/688/kaskus-ramadan",
			"http://www.kaskus.co.id/forum/437/domestik",
			"http://www.kaskus.co.id/forum/669/cerita-pejalan-domestik",
			"http://www.kaskus.co.id/forum/439/mancanegara",
			"http://www.kaskus.co.id/forum/670/cerita-pejalan-mancanegara",
			"http://www.kaskus.co.id/forum/193/wedding--family",
			"http://www.kaskus.co.id/forum/429/kids--parenting",
			"http://www.kaskus.co.id/forum/22/buat-latihan-posting",
			"http://www.kaskus.co.id/forum/177/kaskus-plus-lounge",
			"http://www.kaskus.co.id/forum/31/kritik-saran-pertanyaan-seputar-kaskus",
			"http://www.kaskus.co.id/forum/204/jual-beli-feedback-amp-testimonials",
			"http://www.kaskus.co.id/forum/270/blacklist-jual-beli",
			"http://www.kaskus.co.id/forum/136/feedback-amp-testimonial",
			"http://www.kaskus.co.id/forum/271/official-testimonials-jual-beli",
			"http://www.kaskus.co.id/forum/745/peraturan-jual-beli",
			"http://www.kaskus.co.id/forum/566/surat-terbuka-jual-beli",
			"http://www.kaskus.co.id/forum/272/tips--tutorial-jual-beli",
			"http://www.kaskus.co.id/forum/544/young-on-top-kaskus-community-yotkc"
		]

		for category in self.categories:
			yield Task("category", url=category)

	def task_category(self, grab, task):
		for thread in grab.doc.select(self.thread_link_xpath):
			thread_link = thread.attr("href")
			thread_link = grab.make_url_absolute(thread_link)
			yield Task("get_last_page", url=thread_link, category=task.url)

	def task_get_last_page(self, grab, task):
		element 	   = grab.doc.select(self.last_page_xpath).one()
		last_page_link = element.attr("href")
		last_page_link = grab.make_url_absolute(last_page_link)
		yield Task("crawl", url=last_page_link, category=task.category, thread=task.url)

	def task_crawl(self, grab, task):
		try:
			elements = grab.doc.select(self.post_xpath)

			for element in elements:
				post_element   = XpathSelector(element.node())
				permalink      = post_element.select(self.permalink_xpath).attr("href")
				published_date = post_element.select(self.published_date_xpath).attr("datetime")
				
				post           		= Post()
				post.title          = post_element.select(self.title_xpath).text()
				post.content        = post_element.select(self.content_xpath).text()
				post.author_name    = post_element.select(self.author_name_xpath).text()
				post.published_date = arrow.get(published_date).datetime
				post.permalink      = grab.make_url_absolute(permalink)
				post.crawler        = self.crawler_name
				post.category       = task.category
				post.thread         = task.thread
				post.country        = self.country
				self.saver.save(post)
				print("[success] Inserted one document!")

			prev_page_element = grab.doc.select("//a[re:test(@class,'previous-page')]")
			prev_page_link    = prev_page_element.attr("href")
			prev_page_link    = grab.make_url_absolute(prev_page_link)
			yield Task("crawl", url=prev_page_link, category=task.category, thread=task.url)
		except DuplicateDocument as ex:
			print("[error] %s" % ex)


def run_pool(args):
	saver = SaverFactory.get_saver(SaverFactory.POST)
	bot   = KaskusSpider(thread_number=2, args=(saver,))
	bot.run()

if __name__ == "__main__":
	data = [1]
	with multiprocessing.Pool(1) as pool:
		pool.map(run_pool, data)