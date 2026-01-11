import time
import numpy as np
from os import getenv
from django.core.management.base import BaseCommand
from django.db import transaction

from projects.models import ContentModel


class Command(BaseCommand):
    help = "Generate embeddings for ContentModel records (OpenRouter)"

    def add_arguments(self, parser):
        parser.add_argument("--batch-size", type=int, default=32)
        parser.add_argument(
            "--every-content",
            action="store_true",
            help="Reset all embeddings before re-embedding",
        )

    def handle(self, *args, **options):
        from chatwithme.llm_tools.utils import get_embedder
        batch_size = options["batch_size"]
        every_content = options["every_content"]

        if every_content:
            self.stdout.write("Resetting all embeddings to NULL...")
            ContentModel.objects.update(embedding=None)

        qs = ContentModel.objects.filter(embedding__isnull=True)
        total = qs.count()

        if total == 0:
            self.stdout.write(self.style.SUCCESS("No records need embedding."))
            return

        embedder = get_embedder

        start_time = time.perf_counter()
        processed = 0

        while qs.exists():
            batch = list(qs[:batch_size])

            texts = [
                f"{obj.title}\n{obj.text}"
                for obj in batch
            ]

            vectors = embedder(texts)
            vectors = np.asarray(vectors, dtype="float32")

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
