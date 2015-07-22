from .base import BaseCommand


class IndicesValidateQueryCommand(BaseCommand):
    command_name = "elasticsearch:indices-validate-query"

    def run_request(self):
        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text(),
            params=dict(explain=True)
        )

        return self.client.indices.validate_query(**options)
