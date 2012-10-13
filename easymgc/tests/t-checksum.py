from easymgc import checksum
fn = 'tmp/download/49e2bbda3312c7e7de9d240d3b7edfb92452ba065939f13f6a13b84873841b82-other.sqlite.bz2'



print checksum.perform_checksum(fn, 'size')

print checksum.sha256hash(fn)

print checksum.perform_checksum(fn, 'SHA256')

print checksum.perform_all(fn)