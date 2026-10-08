"""Shared policy for local figures and attributed Wikimedia original images."""
from pathlib import PurePosixPath
from urllib.parse import urlsplit

def figure_source(item):
    local = str(item.get('asset_path') or '')
    remote = str(item.get('image_url') or '')
    if bool(local) == bool(remote):
        raise ValueError('Figure requires exactly one local asset or remote image')
    if local:
        path = PurePosixPath(local)
        if not local.startswith('assets/figures/') or '..' in path.parts or path.suffix.lower() not in {'.svg','.png','.jpg','.webp'}:
            raise ValueError('Figure must use a local assets/figures path')
        return '../../../' + local
    url = urlsplit(remote)
    if (url.scheme != 'https' or url.netloc != 'upload.wikimedia.org' or url.query or url.fragment
            or not url.path.startswith('/wikipedia/commons/') or '..' in url.path.split('/')
            or '%' in url.path or PurePosixPath(url.path).suffix.lower() not in {'.png','.jpg','.webp'}):
        raise ValueError('External figures require a direct HTTPS Wikimedia original image')
    for field in ('source_page_url', 'license_url'):
        link = urlsplit(str(item.get(field) or ''))
        if link.scheme != 'https' or not link.netloc or link.username or link.password:
            raise ValueError('External figures require HTTPS provenance and license links')
    return remote
