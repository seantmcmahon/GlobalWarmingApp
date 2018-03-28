from __future__ import absolute_import, print_function
import sys
from os.path import join, sep
from shutil import rmtree
from os import walk, listdir
from .common import *

__version__ = '0.1.12'

gst_ver = '1.10.2'


def get_gstreamer(cache, build_path, arch, pyver, package, output, compiler='mingw'):
    data = []
    bitness = 'x86_64' if arch == '64' else 'x86'
    runtime_name = 'gstreamer-1.0-{}-{}.msi'.format(bitness, gst_ver)
    devel_name = 'gstreamer-1.0-devel-{}-{}.msi'.format(bitness, gst_ver)

    gst = join(build_path, package)
    makedirs(gst)

    for name in (runtime_name, devel_name):
        url = (
            'https://gstreamer.freedesktop.org/data/pkg/windows/{}/{}'.format(gst_ver, name))
        local_url = download_cache(cache, url, build_path)

        exec_binary(
            "Extracting {} to {}".format(local_url, gst),
            ['msiexec', '/a', local_url, '/qb', 'TARGETDIR={}'.format(gst)],
            cwd=gst, shell=False)
    gst = join(gst, 'gstreamer')
    gst = join(gst, list(listdir(gst))[0], bitness)

    pkg_url = 'pkg-config_0.28-1_win{}.zip'.format('64' if arch == '64' else '32')
    url = 'http://win32builder.gnome.org/packages/3.6/{}'.format(pkg_url)
    local_url = download_cache(cache, url, build_path)

    base_dir = join(build_path, splitext(pkg_url)[0])
    makedirs(base_dir)
    with open(local_url, 'rb') as fd:
        ZipFile(fd).extractall(base_dir)

    data.append((join(base_dir, 'bin', 'pkg-config.exe'), 'pkg-config.exe',
                 'Scripts', True))

    inc = join(gst, 'include')
    for f in listdir(inc):
        if f in ('glib-2.0', 'gstreamer-1.0'):
            continue
        f = join(inc, f)
        if isdir(f):
            rmtree(f)
        else:
            remove(f)

    gstreamer = join(inc, 'gstreamer-1.0')
    for f in listdir(gstreamer):
        if f == 'gst':
            continue
        f = join(gstreamer, f)
        if isdir(f):
            rmtree(f)
        else:
            remove(f)
    gstinc = join(gstreamer, 'gst')
    for f in listdir(gstinc):
        f = join(gstinc, f)
        if isdir(f):
            rmtree(f)

    lib_files = [
        ['gio'],
        ['glib-2.0'],
        ['gstreamer-1.0'],
        ['glib-2.0.lib'],
        ['gmodule-2.0.lib'],
        ['gobject-2.0.lib'],
        ['gstreamer-1.0.lib'],
        ['intl.lib'],
        ['libglib-2.0.dll.a'],
        ['libglib-2.0.la'],
        ['libgmodule-2.0.dll.a'],
        ['libgmodule-2.0.la'],
        ['libgobject-2.0.dll.a'],
        ['libgobject-2.0.la'],
        ['libgstreamer-1.0.a'],
        ['libgstreamer-1.0.dll.a'],
        ['libgstreamer-1.0.la'],
        ['pkgconfig', 'glib-2.0.pc'],
        ['pkgconfig', 'gmodule-2.0.pc'],
        ['pkgconfig', 'gmodule-no-export-2.0.pc'],
        ['pkgconfig', 'gobject-2.0.pc'],
        ['pkgconfig', 'gstreamer-1.0.pc'],
        ]
    remove_from_dir(join(gst, 'lib'), lib_files)

    move_by_ext(join(gst, 'lib', 'gio'), '.dll', join(gst, 'bin'))
    move_by_ext(join(gst, 'lib', 'gstreamer-1.0'), '.dll', join(gst, 'bin'))
    move_by_ext(join(gst, 'lib', 'glib-2.0'), '.h', join(gst, 'include'))
    rmtree(join(gst, 'lib', 'gio'))
    rmtree(join(gst, 'lib', 'glib-2.0'))
    rmtree(join(gst, 'lib', 'gstreamer-1.0'))

    items = list(listdir(gst))
    items.remove('include')
    items.remove('lib')

    for d in ('lib', 'include'):
        src = join(gst, d)
        for dirpath, dirnames, filenames in walk(src):
            root = dirpath
            dirpath = dirpath.replace(src, '').strip(sep)
            inc_dirpath = dirpath
            if d == 'include':
                # for these, copy the contents but not the high level directory
                if inc_dirpath.startswith('glib-2.0'):
                    inc_dirpath = inc_dirpath[8:].strip(sep)
                if inc_dirpath.startswith('gstreamer-1.0'):
                    inc_dirpath = inc_dirpath[13:].strip(sep)

            for filename in filenames:
                data.append((
                    join(root, filename), join(d, dirpath, filename),
                    join('libs' if d == 'lib' else d, inc_dirpath), True))

    for d in items:
        src = join(gst, d)
        for dirpath, dirnames, filenames in walk(src):
            root = dirpath
            dirpath = dirpath.replace(src, '')
            if dirpath and dirpath[0] == sep:
                dirpath = dirpath[1:]

            for filename in filenames:
                data.append((
                    join(root, filename), join('gstreamer', d, dirpath, filename),
                    join('share', package, d, dirpath), False))

                if filename in ('libintl-8.dll', 'libglib-2.0-0.dll'):
                    data.append((join(root, filename), filename, 'Scripts', True))

    l_imports = 'from os import environ'
    l_code = '''
if dep_bins and isdir(dep_bins[0]):
    if environ.get('GST_PLUGIN_PATH'):
        environ['GST_PLUGIN_PATH'] = '{};{}'.format(environ['GST_PLUGIN_PATH'], dep_bins[0])
    else:
        environ['GST_PLUGIN_PATH'] = dep_bins[0]

    if not environ.get('GST_REGISTRY'):
        environ['GST_REGISTRY'] = join(dirname(dep_bins[0]), 'registry.bin')
'''

    make_package(join(build_path, 'project'), package, data, __version__, output,
                 'LGPL', (l_imports, l_code))


if __name__ == '__main__':
    parse_args(get_gstreamer)
