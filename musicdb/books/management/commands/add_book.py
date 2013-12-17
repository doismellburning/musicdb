from django.core.management.base import CommandError, make_option

from musicdb.utils.commands import AddFilesCommand

from musicdb.common.models import File

from ...utils import guess_book_details
from ...models import Author, Book

class Command(AddFilesCommand):
    option_list = AddFilesCommand.option_list + (
        make_option('-a', '--amazon-import', dest='amazon_import', default=False,
            action='store_true', help="Try and populate from Amazon"),
        make_option('-f', '--author-first-names', dest='first_names', default=None,
            action='store', help="Author first names (optional)"),
        make_option('-l', '--author-last-name', dest='last_name', default='',
            action='store', help="Author last name (optional)"),
        make_option('-t', '--title', dest='title', default='',
            action='store', help="Title (optional)"),
    )

    def handle_filenames(self, filenames):
        if len(filenames) != 1:
            raise CommandError("Must specify one file")

        filename = filenames[0]

        if not filename.lower().endswith('.mobi'):
            raise CommandError("Only .mobi files are supported.")

        if self.options['amazon_import']:
            data = guess_book_details(filename)

            if not data:
                raise CommandError("Could not guess book details")

            self.options.update(data)

        last_name = self.options['last_name']
        if not last_name:
            last_name = self.prompt_string(
                "Author last name",
                Author.objects.all(),
                'last_name',
            )

        qs = Author.objects.filter(last_name=last_name)

        try:
            default = qs[0].first_names
        except IndexError:
            default = ''

        first_names = ''
        if self.options['first_names'] is None:
            first_names = self.prompt_string(
                'Author forenames',
                qs,
                'first_names',
                default,
            )

        author, _ = Author.objects.get_or_create(
            last_name=last_name,
            first_names=first_names,
        )

        title = self.options['title']

        if not title:
            title = self.prompt_string(
                'Title',
                author.books.all(),
                'title',
                '',
            )

        book = Book.objects.create(title=title)
        book.authors.create(num=1, author=author)

        file_ = File.objects.create_from_path(
            filenames[0],
            'books/%d/01.mobi' % book.pk,
        )

        book.files.create(file=file_)

        print "I: Added: %s" % book
