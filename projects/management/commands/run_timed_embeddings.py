import time
from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer
from django.db import transaction

from projects.models import ContentModel


class Command(BaseCommand):
    help = "Generate embeddings for ContentModel records with timing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=32,
            help="Number of records per batch",
        )

    def handle(self, *args, **options):
        batch_size = options["batch_size"]

        qs = ContentModel.objects.filter(embedding__isnull=True)
        total = qs.count()

        if total == 0:
            self.stdout.write(self.style.SUCCESS("No records need embedding."))
            return

        model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

        start_time = time.perf_counter()
        processed = 0

        while qs.exists():
            batch = list(qs[:batch_size])

            texts = [
                f"{obj.title}\n{obj.text}"
                for obj in batch
            ]

            vectors = model.encode(
                texts,
                convert_to_numpy=True,
                batch_size=batch_size,
            )

            with transaction.atomic():
                for obj, vec in zip(batch, vectors):
                    obj.embedding = vec.tolist()
                    obj.save(update_fields=["embedding"])

            processed += len(batch)
            elapsed = time.perf_counter() - start_time

            self.stdout.write(
                f"Processed {processed}/{total} "
                f"({elapsed:.2f}s, avg {(elapsed/processed):.4f}s/item)"
            )

        total_elapsed = time.perf_counter() - start_time
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. {processed} records in {total_elapsed:.2f}s"
            )
        )
