from django.core.management.base import BaseCommand

from documents.models import Document, Correspondent

from ...mixins import Renderable


class Command(Renderable, BaseCommand):

    help = """
        Using the current set of tagging rules, apply said rules to all
        documents in the database, effectively allowing you to back-tag all
        previously indexed documents with tags created (or modified) after
        their initial import.
    """.replace("    ", "")

    def __init__(self, *args, **kwargs):
        self.verbosity = 0
        BaseCommand.__init__(self, *args, **kwargs)

    def handle(self, *args, **options):

        self.verbosity = options["verbosity"]

        for document in Document.objects.filter(correspondent=None):
            correspondents = Correspondent.objects.all()
            correspondent = Correspondent.match_first(document.content,
                                                      correspondents)
            print('Set {} on "{}"'.format(correspondent, document))
            document.correspondent = correspondent
            document.save()
