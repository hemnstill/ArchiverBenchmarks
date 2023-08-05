import unittest

from ArchiverCommon import artifact_tools, models


def artifacts_data() -> dict[str, models.ArtifactInfo]:
    return {
        '13MB.zip': models.ArtifactInfo(name='13MB.zip', size=13748886, files_count=2056),
        '116MB.zip': models.ArtifactInfo(name='116MB.zip', size=122518995, files_count=2123),
        '1GB.zip': models.ArtifactInfo(name='git-sdk-64-main.zip', size=1407960952, files_count=108168),
    }


class CompressTests(unittest.TestCase):

    def test_create(self):
        zip_artifact = artifacts_data()['13MB.zip']
        tar_artifact = artifact_tools.create_tar_artifact(zip_artifact)