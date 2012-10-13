SANDBOX_BINARY           = "/usr/bin/sandbox"
FAKEROOT_BINARY          = "/usr/bin/fakeroot"
BASH_BINARY              = "/bin/bash"
PRELINK_BINARY           = "/usr/sbin/prelink"


HASHING_BLOCKSIZE        = 32768
# MANIFEST1_HASH_FUNCTIONS = ("MD5", "SHA256", "RMD160")
# MANIFEST1_REQUIRED_HASH  = "MD5"

# # Future events:
# #
# # After WHIRLPOOL is supported in stable portage:
# # - Add SHA256 and WHIRLPOOL to MANIFEST2_HASH_DEFAULTS.
# # - Remove SHA1 and RMD160 from MANIFEST2_HASH_*.
# # - Set manifest-hashes in gentoo-x86/metadata/layout.conf as follows:
# #     manifest-hashes = SHA256 SHA512 WHIRLPOOL
# #
# # After WHIRLPOOL is supported in stable portage for at least 1 year:
# # - Change MANIFEST2_REQUIRED_HASH to WHIRLPOOL.
# # - Remove SHA256 from MANIFEST2_HASH_*.
# # - Set manifest-hashes in gentoo-x86/metadata/layout.conf as follows:
# #     manifest-hashes = SHA512 WHIRLPOOL
# #
# # After SHA-3 is approved:
# # - Add new hashes to MANIFEST2_HASH_*.
# #
# # After SHA-3 is supported in stable portage:
# # - Set manifest-hashes in gentoo-x86/metadata/layout.conf as follows:
# #     manifest-hashes = SHA3 SHA512 WHIRLPOOL
# #
# # After layout.conf settings correspond to defaults in stable portage:
# # - Remove redundant settings from gentoo-x86/metadata/layout.conf.

# MANIFEST2_HASH_FUNCTIONS = ("RMD160", "SHA1", "SHA256", "SHA512", "WHIRLPOOL")
# MANIFEST2_HASH_DEFAULTS = frozenset(["SHA1", "SHA256", "RMD160"])
# MANIFEST2_REQUIRED_HASH  = "SHA256"

# MANIFEST2_IDENTIFIERS    = ("AUX", "MISC", "DIST", "EBUILD")
