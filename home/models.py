from django.db import models
from django.conf import settings
from wagtail.models import Page, Orderable, Collection
from wagtail.fields import RichTextField
from wagtail.admin.panels import (
    FieldPanel, InlinePanel, FieldRowPanel,
    TabbedInterface, ObjectList
)
from wagtail.images.models import Image
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from django.core.cache import cache
from django.conf import settings
import requests

# Event Index Page
class EventIndexPage(Page):
    max_count = 1
    subpage_types = ["home.HomePage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["events"] = HomePage.objects.live().public().order_by("-year")
        context["latest_event"] = context["events"].first()
        return context

# HomePage
class HomePage(Page):
    parent_page_types = ["home.EventIndexPage"]
    subpage_types = [
        "home.AlbumPage",
        "home.PlaylistPage",
        "home.NewsPage",
    ]
    year = models.IntegerField(unique=True)
    hero_image = models.ForeignKey(
        Image, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )
    heading = models.CharField(max_length=250, blank=True)
    date = models.CharField(max_length=100, blank=True)

    event_datetime = models.DateTimeField()
    intro = RichTextField(blank=True)

    footer_heading = models.CharField(max_length=255, blank=True)
    footer_bottom_text = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("year"),
        FieldPanel("hero_image"),
        FieldPanel("heading"),
        FieldPanel("date"),
        FieldPanel("event_datetime"),
        FieldPanel("intro"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Introduction"),
        ObjectList([
            InlinePanel("organizers", label="मुख्य आयोजकहरू (Top Cards)"),
            InlinePanel("organizer_members", label="दुज सदस्यहरू (Member List)"),
        ], heading="🎤 Organizers"),
        ObjectList([
            InlinePanel("literary_winner_categories", label="साहित्य विधा (Literary Winners)"),
        ], heading="🏆 Literary Winners"),
        ObjectList([
            InlinePanel("cultural_winner_categories", label="सांस्कृतिक विधा (Cultural Winners)"),
        ], heading="🎭 Cultural Winners"),
        ObjectList([
            InlinePanel("albums", label="Albums"),
        ], heading="🖼️ Albums"),
        ObjectList([
            InlinePanel("playlists", label="Playlists"),
        ], heading="🎬 Playlists"),
        ObjectList([
            InlinePanel("news_items", label="समाचार"),
        ], heading="📰 News"),
        ObjectList([
            InlinePanel("venues", label="Venue"),
        ], heading="📍Venue"),
        ObjectList([
            FieldPanel("footer_heading"),
            InlinePanel("footer_contacts", label="Footer Contacts"),
            FieldPanel("footer_bottom_text"),
        ], heading="🔻Footer"),

    ])

    def get_context(self, request):
        context = super().get_context(request)

        # LAST 6 news items, latest first
        context["latest_news"] = (
            self.news_items
            .order_by("-sort_order")[:6]
        )


        context["news_page"] = (
            self.get_children()
            .type(NewsPage)
            .live()
            .first()
        )

        # All HomePages (for year switcher)
        context["all_years"] = (
            HomePage.objects.live().public().order_by("-year")
        )

        return context
    
    
# 🔹 Organizer Card (top 6 cards)
class OrganizerItem(Orderable):
    page = ParentalKey(HomePage, related_name="organizers", on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=50, blank=True)

    panels = [
        FieldRowPanel([
            FieldPanel("position"),
            FieldPanel("name"),
            FieldPanel("phone"),
        ])
    ]

    def __str__(self):
        return f"{self.position} - {self.name}"


# 🔹 General Members (दुज section)
class OrganizerMember(Orderable):
    page = ParentalKey(HomePage, related_name="organizer_members", on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    panels = [FieldPanel("name")]

    def __str__(self):
        return self.name
    
# Winner Section
# 🟨 1. Literary Winner Category (कविता, कथा, निबन्ध)
class LiteraryWinnerCategory(Orderable, ClusterableModel):
    page = ParentalKey(
        "home.HomePage",
        related_name="literary_winner_categories",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100, help_text="e.g., कविता, कथा, निबन्ध")

    panels = [
        FieldPanel("title"),
        InlinePanel("literary_winner_entries", label="Literary Winners"),
    ]

    def __str__(self):
        return self.title


# 🟩 2. Literary Winner Entry
class LiteraryWinnerEntry(Orderable):
    category = ParentalKey(
        LiteraryWinnerCategory,
        related_name="literary_winner_entries",
        on_delete=models.CASCADE
    )
    position = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    subject = models.CharField(max_length=200, blank=True)
    youtube_link = models.URLField(blank=True)

    panels = [
        FieldRowPanel([
            FieldPanel("position"),
            FieldPanel("name"),
            FieldPanel("subject"),
        ]),
        FieldPanel("youtube_link"),
    ]

    def __str__(self):
        return f"{self.position} — {self.name}"


# 🟥 3. Cultural Winner Category (नाच, नाटक, ख्याल)
class CulturalWinnerCategory(Orderable, ClusterableModel):
    page = ParentalKey(
        "home.HomePage",
        related_name="cultural_winner_categories",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100, help_text="e.g., छधाप्याखँ, ख्याल, विशेष सिरपा, हुलाप्याखँ ")

    panels = [
        FieldPanel("title"),
        InlinePanel("cultural_winner_entries", label="Cultural Winners"),
    ]

    def __str__(self):
        return self.title


# 🟦 4. Cultural Winner Entry
class CulturalWinnerEntry(Orderable):
    category = ParentalKey(
        CulturalWinnerCategory,
        related_name="cultural_winner_entries",
        on_delete=models.CASCADE
    )
    position = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    subject = models.CharField(max_length=200, blank=True)
    youtube_link = models.URLField(blank=True)

    panels = [
        FieldRowPanel([
            FieldPanel("position"),
            FieldPanel("name"),
            FieldPanel("subject"),
        ]),
        FieldPanel("youtube_link"),
    ]

    def __str__(self):
        return f"{self.position} — {self.name}"
    

# 🟦 Album Item (not a Page, but part of HomePage tab)
class AlbumItem(Orderable):
    page = ParentalKey(
        "home.HomePage",
        related_name="albums",
        on_delete=models.CASCADE
    )

    title_nepali = models.CharField(max_length=200, blank=True)

    album_page = models.ForeignKey(
        "home.AlbumPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Select the album page to link"
    )

    thumbnail = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Album cover image (16:9 recommended)"
    )

    panels = [
        FieldPanel("title_nepali"),
        FieldPanel("album_page"),
        FieldPanel("thumbnail"),
    ]


class AlbumPage(Page):
    """Displays all images from a specific collection (album)."""
    parent_page_types = ["home.HomePage"]
    template = "home/album_page.html"
    collection = models.ForeignKey(
        Collection,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="This album will display images from the selected collection."
    )

    content_panels = Page.content_panels + [
        FieldPanel("collection"),
    ]

    def get_images(self):
        """Return all images from this page's collection."""
        if self.collection:
            return Image.objects.filter(collection=self.collection)
        return []
    
    def __str__(self):
        return self.title
    


class PlaylistItem(Orderable):
    page = ParentalKey(
        "home.HomePage",
        related_name="playlists",
        on_delete=models.CASCADE
    )

    playlist_title = models.CharField(max_length=255)
    playlist_page = models.ForeignKey(
        "home.PlaylistPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    thumbnail = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        FieldPanel("playlist_title"),
        FieldPanel("playlist_page"),
        FieldPanel("thumbnail"),

    ]

    def __str__(self):
        return self.playlist_title

    
class PlaylistPage(Page):
    parent_page_types = ["home.HomePage"]
    template = "home/playlist_page.html"

    # playlist_title = models.CharField(max_length=255) most editors hate duplicate titles
    playlist_id = models.CharField(max_length=100)

    content_panels = Page.content_panels + [
        # FieldPanel("playlist_title"),
        FieldPanel("playlist_id"),
    ]


    def get_videos(self):
        """
        Fetch videos from YouTube playlist with caching.
        Cache duration: 1 hour
        """

        cache_key = f"playlist_videos_{self.playlist_id}"
        cached_videos = cache.get(cache_key)

        if cached_videos is not None:
            return cached_videos

        videos = []

        if not self.playlist_id:
            return videos

        url = "https://www.googleapis.com/youtube/v3/playlistItems"
        params = {
            "part": "snippet",
            "playlistId": self.playlist_id,
            "maxResults": 50,
            "key": settings.YOUTUBE_API_KEY,
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            # API error / network issue → return empty list safely
            return videos

        for item in data.get("items", []):
            snippet = item.get("snippet", {})
            resource = snippet.get("resourceId")

            # Skip private / deleted videos
            if not resource or resource.get("kind") != "youtube#video":
                continue

            thumbnails = snippet.get("thumbnails", {})

            videos.append({
                "title": snippet.get("title"),
                "video_id": resource.get("videoId"),
                "thumbnail": (
                    thumbnails.get("medium", {}) or
                    thumbnails.get("default", {})
                ).get("url"),
            })

        # Cache result (even if empty to avoid repeat API hits)
        cache.set(cache_key, videos, 60 * 60)  # 1 hour

        return videos

    
class NewsItem(Orderable):
    page = ParentalKey(
        "home.HomePage",
        on_delete=models.CASCADE,
        related_name="news_items"
    )
    link = models.URLField()
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=255)

    panels = [
        FieldPanel("link"),
        FieldRowPanel([
            FieldPanel("title"),
            FieldPanel("source")
        ])
    ]

    def __str__(self):
        return self.title
    
# View more for news
class NewsPage(Page):
    template = "home/news_page.html"
    max_count = 1

    def get_context(self, request):
        context = super().get_context(request)

        home_page = self.get_parent().specific

        context["home_page"] = home_page
        context["all_news"] = home_page.news_items.order_by("-sort_order")

        return context


class VenueItem(Orderable):
    page = ParentalKey(
        "home.HomePage",
        related_name="venues",
        on_delete=models.CASCADE
    )

    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    name = models.CharField(
        max_length=255,
        help_text="Venue name / address"
    )

    map_embed_url = models.URLField(
        max_length=2000,
        blank=True,
        help_text="Google Maps → Share this location → Embed a map → Copy HTML → Extract src"
    )

    map_link = models.URLField(
        max_length=1000,
        blank=True,
        help_text="Google Maps → Share this location → Copy Link"
    )

    panels = [
        FieldPanel("image"),
        FieldPanel("name"),
        FieldPanel("map_embed_url"),
        FieldPanel("map_link"),
    ]

    def __str__(self):
        return self.name
    
class FooterContact(Orderable):
    page = ParentalKey(
        "home.HomePage",
        related_name="footer_contacts",
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=255,
        help_text="Committee / Region title"
    )

    description = models.CharField(
        help_text="Name"
    )

    contact_number = models.CharField(
        max_length=50,
        blank=True,
        help_text="9841604343"
    )

    panels = [
        FieldRowPanel([
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("contact_number"),
        ]),
    ]

    def __str__(self):
        return self.title