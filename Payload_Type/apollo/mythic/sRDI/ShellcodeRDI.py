import sys

if sys.version_info < (3,0):
    print("[!] Sorry, requires Python 3.x")
    sys.exit(1)
    
import struct
from struct import pack

MACHINE_IA64=512
MACHINE_AMD64=34404

def is64BitDLL(bytes):
    header_offset = struct.unpack("<L", bytes[60:64])[0]
    machine = struct.unpack("<H", bytes[header_offset+4:header_offset+4+2])[0]
    if machine == MACHINE_IA64 or machine == MACHINE_AMD64:
        return True   
    return False
    
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

def HashFunctionName(name, module = None):

        function = name.encode() + b'\x00'

        if(module):
                module = module.upper().encode('UTF-16LE') + b'\x00\x00'

                functionHash = 0

                for b in function:
                        functionHash = ror(functionHash, 13, 32)
                        functionHash += b

                moduleHash = 0

                for b in module:
                        moduleHash = ror(moduleHash, 13, 32)
                        moduleHash += b

                functionHash += moduleHash

                if functionHash > 0xFFFFFFFF: functionHash -= 0x100000000

        else:
                functionHash = 0

                for b in function:
                        functionHash = ror(functionHash, 13, 32)
                        functionHash += b

        return functionHash

def ConvertToShellcode(dllBytes, functionHash=0x10, userData=b'None', flags=0):

    #MARKER:S
    rdiShellcode32 = b'\x83\xEC\x6C\x53\x55\x56\x57\xB9\x4C\x77\x26\x07\xE8\x6E\x06\x00\x00\x8B\xF8\xB9\x49\xF7\x02\x78\x89\x7C\x24\x28\xE8\x5E\x06\x00\x00\x8B\xF0\xB9\x58\xA4\x53\xE5\x89\x74\x24\x2C\xE8\x4E\x06\x00\x00\x8B\xD8\xB9\x10\xE1\x8A\xC3\x89\x5C\x24\x20\xE8\x3E\x06\x00\x00\xB9\xAF\xB1\x5C\x94\x89\x44\x24\x30\xE8\x30\x06\x00\x00\xB9\x33\x00\x9E\x95\x89\x44\x24\x34\xE8\x22\x06\x00\x00\xB9\x44\xF0\x35\xE0\x8B\xE8\xE8\x16\x06\x00\x00\x89\x44\x24\x40\x85\xFF\x0F\x84\x00\x06\x00\x00\x85\xF6\x0F\x84\xF8\x05\x00\x00\x85\xDB\x0F\x84\xF0\x05\x00\x00\x83\x7C\x24\x30\x00\x0F\x84\xE5\x05\x00\x00\x83\x7C\x24\x34\x00\x0F\x84\xDA\x05\x00\x00\x85\xED\x0F\x84\xD2\x05\x00\x00\x85\xC0\x0F\x84\xCA\x05\x00\x00\x8B\x84\x24\x80\x00\x00\x00\x8B\x70\x3C\x03\xF0\x81\x3E\x50\x45\x00\x00\x0F\x85\xB2\x05\x00\x00\xB8\x4C\x01\x00\x00\x66\x39\x46\x04\x0F\x85\xA3\x05\x00\x00\xF6\x46\x38\x01\x0F\x85\x99\x05\x00\x00\x0F\xB7\x56\x06\x33\xFF\x0F\xB7\x46\x14\x85\xD2\x74\x22\x8D\x4E\x24\x03\xC8\x83\x79\x04\x00\x8B\x01\x75\x05\x03\x46\x38\xEB\x03\x03\x41\x04\x3B\xC7\x0F\x47\xF8\x83\xC1\x28\x83\xEA\x01\x75\xE3\x8D\x44\x24\x58\x50\xFF\xD5\x8B\x4C\x24\x5C\x8D\x51\xFF\x8D\x69\xFF\xF7\xD2\x03\x6E\x50\x8D\x41\xFF\x03\xC7\x23\xEA\x23\xC2\x3B\xE8\x0F\x85\x42\x05\x00\x00\x6A\x04\xBF\x00\x30\x00\x00\x57\x55\xFF\x76\x34\xFF\xD3\x8B\xD8\x89\x5C\x24\x24\x85\xDB\x75\x0F\x6A\x04\x57\x55\x50\xFF\x54\x24\x30\x8B\xD8\x89\x44\x24\x24\xF6\x84\x24\x90\x00\x00\x00\x01\x74\x28\x8B\x94\x24\x80\x00\x00\x00\x8B\x42\x3C\x89\x43\x3C\x8B\x4A\x3C\x3B\x4E\x54\x73\x31\x8D\x3C\x0B\x2B\xD3\x8A\x04\x3A\x41\x88\x07\x47\x3B\x4E\x54\x72\xF4\xEB\x1E\x33\xFF\x39\x7E\x54\x76\x17\x8B\x94\x24\x80\x00\x00\x00\x8B\xCB\x2B\xD3\x8A\x04\x11\x47\x88\x01\x41\x3B\x7E\x54\x72\xF4\x8B\x6B\x3C\x33\xC9\x03\xEB\x89\x4C\x24\x1C\x33\xD2\x89\x6C\x24\x14\x0F\xB7\x45\x14\x66\x3B\x55\x06\x73\x40\x8D\x75\x28\x03\xF0\x33\xFF\x39\x3E\x76\x25\x8B\xAC\x24\x80\x00\x00\x00\x8B\x46\x04\x8D\x14\x3B\x8B\x4E\xFC\x03\xC7\x47\x8A\x04\x28\x88\x04\x0A\x3B\x3E\x72\xEA\x8B\x6C\x24\x14\x8B\x4C\x24\x1C\x0F\xB7\x45\x06\x41\x83\xC6\x28\x89\x4C\x24\x1C\x3B\xC8\x72\xC5\x6A\x01\x8B\xFB\x5E\x89\x74\x24\x20\x2B\x7D\x34\x74\x7B\x83\xBD\xA4\x00\x00\x00\x00\x74\x72\x8B\x95\xA0\x00\x00\x00\x03\xD3\x83\x3A\x00\x74\x65\x6A\x02\x5D\x8D\x72\x08\xEB\x46\x0F\xB7\x0E\x66\x8B\xC1\x66\xC1\xE8\x0C\x66\x83\xF8\x0A\x74\x06\x66\x83\xF8\x03\x75\x0D\x81\xE1\xFF\x0F\x00\x00\x03\x0A\x01\x3C\x19\xEB\x21\x66\x3B\x44\x24\x20\x75\x07\x8B\xC7\xC1\xE8\x10\xEB\x08\x66\x3B\xC5\x75\x0E\x0F\xB7\xC7\x81\xE1\xFF\x0F\x00\x00\x03\x0A\x01\x04\x19\x03\xF5\x8B\x42\x04\x03\xC2\x3B\xF0\x75\xB1\x83\x3E\x00\x8B\xD6\x75\xA5\x8B\x6C\x24\x14\x33\xF6\x46\x83\xBD\x84\x00\x00\x00\x00\x0F\x84\x97\x01\x00\x00\x8B\x85\x80\x00\x00\x00\x8D\x0C\x18\x83\xC0\x0C\x03\xC3\x89\x4C\x24\x1C\x33\xC9\x89\x4C\x24\x18\x39\x08\x74\x0D\x8D\x40\x14\x41\x83\x38\x00\x75\xF7\x89\x4C\x24\x18\x8B\x94\x24\x90\x00\x00\x00\x8B\xC2\x83\xE0\x04\x89\x44\x24\x3C\x0F\x84\xAE\x00\x00\x00\x3B\xCE\x0F\x86\xA6\x00\x00\x00\xC1\xEA\x10\x8D\x41\xFF\x89\x94\x24\x90\x00\x00\x00\x33\xD2\x89\x44\x24\x38\x89\x54\x24\x20\x85\xC0\x0F\x84\x92\x00\x00\x00\x8B\x5C\x24\x1C\x8B\xAC\x24\x80\x00\x00\x00\x89\x5C\x24\x1C\x2B\xCA\x69\xED\xFD\x43\x03\x00\x33\xD2\x8D\x7C\x24\x44\xB8\xFF\x7F\x00\x00\xF7\xF1\x81\xC5\xC3\x9E\x26\x00\x33\xD2\x6A\x05\x8D\x48\x01\x8B\xC5\xC1\xE8\x10\x25\xFF\x7F\x00\x00\xF7\xF1\x8B\x54\x24\x24\x03\xC2\x6B\xC0\x14\x59\x6A\x05\x03\xC3\x42\x8B\xF0\x89\x54\x24\x24\xF3\xA5\x8B\x74\x24\x20\x8B\xF8\x8B\x44\x24\x20\x59\xF3\xA5\x6A\x05\x8B\xF8\x8D\x74\x24\x48\x59\x83\xC0\x14\xF3\xA5\x8B\x4C\x24\x18\x89\x44\x24\x1C\x3B\x54\x24\x38\x72\x92\x8B\x5C\x24\x24\x8B\x6C\x24\x14\xEB\x0B\x8B\x44\x24\x40\x89\x84\x24\x90\x00\x00\x00\x8B\xB5\x80\x00\x00\x00\x03\xF3\x89\x74\x24\x20\x8B\x46\x0C\x85\xC0\x0F\x84\x88\x00\x00\x00\x8B\x6C\x24\x18\x03\xC3\x50\xFF\x54\x24\x2C\x8B\x7E\x10\x89\x44\x24\x38\x03\xFB\x8B\x06\x03\xC3\x89\x44\x24\x24\x8B\x08\x85\xC9\x74\x36\x8B\x6C\x24\x38\x8B\x74\x24\x2C\x79\x05\x0F\xB7\xC1\xEB\x05\x8D\x41\x02\x03\xC3\x50\x55\xFF\xD6\x89\x07\x83\xC7\x04\x8B\x44\x24\x24\x83\xC0\x04\x89\x44\x24\x24\x8B\x08\x85\xC9\x75\xDA\x8B\x74\x24\x20\x8B\x6C\x24\x18\x83\x7C\x24\x3C\x00\x74\x17\x33\xC0\x40\x3B\xE8\x76\x10\x69\x84\x24\x90\x00\x00\x00\xE8\x03\x00\x00\x50\xFF\x54\x24\x44\x8B\x46\x20\x83\xC6\x14\x89\x74\x24\x20\x85\xC0\x75\x80\x8B\x6C\x24\x14\x83\xBD\xE4\x00\x00\x00\x00\x74\x73\x8B\xBD\xE0\x00\x00\x00\x83\xC7\x04\x03\xFB\x89\x7C\x24\x20\x83\x3F\x00\x74\x5F\x8B\x07\x03\xC3\x50\xFF\x54\x24\x2C\x8B\x77\x08\x8B\xE8\x8B\x47\x0C\x03\xF3\x03\xC3\x89\x44\x24\x24\x83\x3E\x00\x74\x31\x8B\x7C\x24\x2C\x8B\x00\x85\xC0\x79\x05\x0F\xB7\xC0\xEB\x05\x83\xC0\x02\x03\xC3\x50\x55\xFF\xD7\x89\x06\x83\xC6\x04\x8B\x44\x24\x24\x83\xC0\x04\x89\x44\x24\x24\x83\x3E\x00\x75\xD7\x8B\x7C\x24\x20\x83\xC7\x20\x89\x7C\x24\x20\x83\x3F\x00\x75\xA5\x8B\x6C\x24\x14\x0F\xB7\x45\x14\x33\xC9\x33\xFF\x66\x3B\x4D\x06\x0F\x83\xB0\x00\x00\x00\x8D\x75\x3C\x03\xF0\x83\x7E\xEC\x00\x0F\x84\x91\x00\x00\x00\x8B\x0E\x33\xD2\x42\x8B\xC1\xC1\xE8\x1D\x23\xC2\x8B\xD1\xC1\xEA\x1E\x83\xE2\x01\xC1\xE9\x1F\x85\xC0\x75\x18\x85\xD2\x75\x0D\x6A\x08\x58\x6A\x01\x85\xC9\x59\x0F\x44\xC1\xEB\x3D\x6A\x04\x58\x6A\x02\xEB\xF1\x85\xD2\x75\x1E\x85\xC9\x75\x05\x6A\x10\x58\xEB\x29\x85\xD2\x75\x11\x85\xC9\x74\x07\xB8\x80\x00\x00\x00\xEB\x1A\x8B\x44\x24\x10\xEB\x18\x85\xC9\x75\x04\x6A\x20\xEB\xE0\x8B\x44\x24\x10\x85\xC9\x6A\x40\x5A\x0F\x45\xC2\x89\x44\x24\x10\xF7\x06\x00\x00\x00\x04\x74\x09\x0D\x00\x02\x00\x00\x89\x44\x24\x10\x8D\x4C\x24\x10\x51\x50\x8B\x46\xE8\xFF\x76\xEC\x03\xC3\x50\xFF\x54\x24\x40\x0F\xB7\x45\x06\x47\x83\xC6\x28\x3B\xF8\x0F\x82\x55\xFF\xFF\xFF\x6A\x00\x6A\x00\x6A\xFF\xFF\x54\x24\x40\x83\xBD\xC4\x00\x00\x00\x00\x74\x26\x8B\x85\xC0\x00\x00\x00\x8B\x74\x18\x0C\x8B\x06\x85\xC0\x74\x16\x33\xED\x45\x6A\x00\x55\x53\xFF\xD0\x8D\x76\x04\x8B\x06\x85\xC0\x75\xF1\x8B\x6C\x24\x14\x33\xC0\x40\x50\x50\x8B\x45\x28\x53\x03\xC3\xFF\xD0\x83\xBC\x24\x84\x00\x00\x00\x00\x0F\x84\xAD\x00\x00\x00\x83\x7D\x7C\x00\x0F\x84\xA3\x00\x00\x00\x8B\x55\x78\x03\xD3\x8B\x6A\x18\x85\xED\x0F\x84\x93\x00\x00\x00\x83\x7A\x14\x00\x0F\x84\x89\x00\x00\x00\x8B\x7A\x20\x8B\x4A\x24\x03\xFB\x83\x64\x24\x34\x00\x03\xCB\x85\xED\x74\x76\x8B\x37\xC7\x44\x24\x1C\x00\x00\x00\x00\x03\xF3\x74\x68\x8A\x06\x84\xC0\x74\x1C\x8B\x6C\x24\x1C\x0F\xBE\xC0\x03\xC5\xC1\xC8\x0D\x46\x8B\xE8\x8A\x06\x84\xC0\x75\xEF\x89\x6C\x24\x1C\x8B\x6A\x18\x8B\x84\x24\x84\x00\x00\x00\x3B\x44\x24\x1C\x75\x04\x85\xC9\x75\x15\x8B\x44\x24\x34\x83\xC7\x04\x40\x83\xC1\x02\x89\x44\x24\x34\x3B\xC5\x72\xAC\xEB\x20\x0F\xB7\x09\x8B\x42\x1C\xFF\xB4\x24\x8C\x00\x00\x00\xFF\xB4\x24\x8C\x00\x00\x00\x8D\x04\x88\x8B\x04\x18\x03\xC3\xFF\xD0\x59\x59\x8B\xC3\xEB\x02\x33\xC0\x5F\x5E\x5D\x5B\x83\xC4\x6C\xC3\x83\xEC\x10\x64\xA1\x30\x00\x00\x00\x53\x55\x56\x8B\x40\x0C\x57\x89\x4C\x24\x18\x8B\x70\x0C\xE9\x8A\x00\x00\x00\x8B\x46\x30\x33\xC9\x8B\x5E\x2C\x8B\x36\x89\x44\x24\x14\x8B\x42\x3C\x8B\x6C\x10\x78\x89\x6C\x24\x10\x85\xED\x74\x6D\xC1\xEB\x10\x33\xFF\x85\xDB\x74\x1F\x8B\x6C\x24\x14\x8A\x04\x2F\xC1\xC9\x0D\x3C\x61\x0F\xBE\xC0\x7C\x03\x83\xC1\xE0\x03\xC8\x47\x3B\xFB\x72\xE9\x8B\x6C\x24\x10\x8B\x44\x2A\x20\x33\xDB\x8B\x7C\x2A\x18\x03\xC2\x89\x7C\x24\x14\x85\xFF\x74\x31\x8B\x28\x33\xFF\x03\xEA\x83\xC0\x04\x89\x44\x24\x1C\x0F\xBE\x45\x00\xC1\xCF\x0D\x03\xF8\x45\x80\x7D\xFF\x00\x75\xF0\x8D\x04\x0F\x3B\x44\x24\x18\x74\x20\x8B\x44\x24\x1C\x43\x3B\x5C\x24\x14\x72\xCF\x8B\x56\x18\x85\xD2\x0F\x85\x6B\xFF\xFF\xFF\x33\xC0\x5F\x5E\x5D\x5B\x83\xC4\x10\xC3\x8B\x74\x24\x10\x8B\x44\x16\x24\x8D\x04\x58\x0F\xB7\x0C\x10\x8B\x44\x16\x1C\x8D\x04\x88\x8B\x04\x10\x03\xC2\xEB\xDB'
    rdiShellcode64 = b'\x48\x8B\xC4\x48\x89\x58\x08\x44\x89\x48\x20\x4C\x89\x40\x18\x89\x50\x10\x55\x56\x57\x41\x54\x41\x55\x41\x56\x41\x57\x48\x8D\x68\xA9\x48\x81\xEC\x90\x00\x00\x00\x48\x8B\xF1\xB9\x4C\x77\x26\x07\xE8\xA3\x06\x00\x00\xB9\x49\xF7\x02\x78\x48\x89\x45\xB7\x4C\x8B\xE0\xE8\x92\x06\x00\x00\xB9\x58\xA4\x53\xE5\x48\x89\x45\xBF\x4C\x8B\xE8\xE8\x81\x06\x00\x00\xB9\x10\xE1\x8A\xC3\x4C\x8B\xF8\xE8\x74\x06\x00\x00\xB9\xAF\xB1\x5C\x94\x48\x89\x45\xD7\x48\x8B\xF8\xE8\x63\x06\x00\x00\xB9\x33\x00\x9E\x95\x48\x89\x45\xDF\x48\x8B\xD8\xE8\x52\x06\x00\x00\xB9\x44\xF0\x35\xE0\x4C\x8B\xF0\xE8\x45\x06\x00\x00\x45\x33\xD2\x48\x89\x45\xC7\x4D\x85\xE4\x0F\x84\x16\x06\x00\x00\x4D\x85\xED\x0F\x84\x0D\x06\x00\x00\x4D\x85\xFF\x0F\x84\x04\x06\x00\x00\x48\x85\xFF\x0F\x84\xFB\x05\x00\x00\x48\x85\xDB\x0F\x84\xF2\x05\x00\x00\x4D\x85\xF6\x0F\x84\xE9\x05\x00\x00\x48\x85\xC0\x0F\x84\xE0\x05\x00\x00\x48\x63\x7E\x3C\x48\x03\xFE\x81\x3F\x50\x45\x00\x00\x0F\x85\xCD\x05\x00\x00\xB8\x64\x86\x00\x00\x66\x39\x47\x04\x0F\x85\xBE\x05\x00\x00\x44\x8B\x47\x38\x45\x8D\x5A\x01\x45\x84\xC3\x0F\x85\xAD\x05\x00\x00\x0F\xB7\x47\x06\x41\x8B\xDA\x0F\xB7\x4F\x14\x85\xC0\x74\x28\x48\x83\xC1\x24\x44\x8B\xC8\x48\x03\xCF\x8B\x51\x04\x85\xD2\x75\x07\x8B\x11\x41\x03\xD0\xEB\x02\x03\x11\x3B\xD3\x0F\x47\xDA\x48\x83\xC1\x28\x4D\x2B\xCB\x75\xE2\x48\x8D\x4D\xE7\x41\xFF\xD6\x8B\x55\xEB\x44\x8D\x72\xFF\x44\x03\x77\x50\x8D\x42\xFF\xF7\xD0\x48\x8D\x4A\xFF\x44\x23\xF0\x8B\xC3\x48\x03\xC8\x48\x8D\x42\xFF\x48\xF7\xD0\x48\x23\xC8\x4C\x3B\xF1\x0F\x85\x40\x05\x00\x00\x48\x8B\x4F\x30\x41\xB9\x04\x00\x00\x00\x41\xB8\x00\x30\x00\x00\x41\x8B\xD6\x41\xFF\xD7\x48\x8B\xD8\x48\x85\xC0\x75\x15\x44\x8D\x48\x04\x41\xB8\x00\x30\x00\x00\x41\x8B\xD6\x33\xC9\x41\xFF\xD7\x48\x8B\xD8\x44\x8B\x5D\x7F\x41\xBE\x01\x00\x00\x00\x45\x84\xDE\x0F\x84\xB1\x00\x00\x00\x8B\x46\x3C\x89\x43\x3C\x8B\x56\x3C\xEB\x0B\x8B\xCA\x41\x03\xD6\x8A\x04\x31\x88\x04\x19\x3B\x57\x54\x72\xF0\x45\x33\xFF\x48\x63\x7B\x3C\x45\x8B\xD7\x48\x03\xFB\x48\x89\x7D\xCF\x0F\xB7\x47\x14\x66\x44\x3B\x7F\x06\x73\x3E\x4C\x8D\x47\x28\x4C\x03\xC0\x45\x8B\xCF\x45\x39\x38\x76\x1F\x41\x8B\x50\x04\x41\x8B\x48\xFC\x41\x8B\xC1\x45\x03\xCE\x48\x03\xC8\x48\x03\xD0\x8A\x04\x32\x88\x04\x19\x45\x3B\x08\x72\xE1\x0F\xB7\x47\x06\x45\x03\xD6\x49\x83\xC0\x28\x44\x3B\xD0\x72\xC9\x4C\x8B\xD3\x4C\x2B\x57\x30\x0F\x84\xDE\x00\x00\x00\x44\x39\xBF\xB4\x00\x00\x00\x0F\x84\xD1\x00\x00\x00\x44\x8B\x87\xB0\x00\x00\x00\x4C\x03\xC3\x45\x39\x38\x0F\x84\xBE\x00\x00\x00\x41\xBC\x02\x00\x00\x00\x4D\x8D\x48\x08\xE9\x93\x00\x00\x00\x45\x33\xFF\x41\x8B\xD7\x44\x39\x7F\x54\x0F\x86\x5D\xFF\xFF\xFF\x8B\xCA\x41\x03\xD6\x8A\x04\x31\x88\x04\x19\x3B\x57\x54\x72\xF0\xE9\x48\xFF\xFF\xFF\x41\x0F\xB7\x01\x0F\xB7\xC8\x66\xC1\xE9\x0C\x66\x83\xF9\x0A\x75\x11\x41\x8B\x08\x25\xFF\x0F\x00\x00\x48\x03\xC3\x4C\x01\x14\x01\xEB\x49\x66\x83\xF9\x03\x75\x0E\x25\xFF\x0F\x00\x00\x48\x8D\x0C\x03\x41\x8B\xC2\xEB\x2E\x66\x41\x3B\xCE\x75\x15\x25\xFF\x0F\x00\x00\x48\x8D\x0C\x03\x49\x8B\xC2\x48\xC1\xE8\x10\x0F\xB7\xC0\xEB\x13\x66\x41\x3B\xCC\x75\x14\x25\xFF\x0F\x00\x00\x48\x8D\x0C\x03\x41\x0F\xB7\xC2\x41\x8B\x10\x48\x01\x04\x0A\x4D\x03\xCC\x41\x8B\x40\x04\x49\x03\xC0\x4C\x3B\xC8\x75\x86\x4D\x8B\xC1\x45\x39\x39\x0F\x85\x4C\xFF\xFF\xFF\x4C\x8B\x65\xB7\x44\x39\xBF\x94\x00\x00\x00\x0F\x84\x45\x01\x00\x00\x44\x8B\x87\x90\x00\x00\x00\x45\x8B\xEF\x4C\x03\xC3\x49\x8D\x40\x0C\xEB\x07\x45\x03\xEE\x48\x8D\x40\x14\x44\x39\x38\x75\xF4\x41\x8B\xC3\x83\xE0\x04\x89\x45\xB3\x0F\x84\x82\x00\x00\x00\x45\x3B\xEE\x76\x7D\x41\xC1\xEB\x10\x45\x8D\x4D\xFF\x44\x89\x5D\x7F\x45\x8B\xDF\x45\x85\xC9\x74\x6F\x4D\x8B\xD0\x41\x0F\x10\x02\x33\xD2\x41\x8B\xCD\x41\x2B\xCB\x69\xF6\xFD\x43\x03\x00\xB8\xFF\x7F\x00\x00\xF7\xF1\x33\xD2\x81\xC6\xC3\x9E\x26\x00\x41\x8D\x0C\x06\x8B\xC6\xC1\xE8\x10\x25\xFF\x7F\x00\x00\xF7\xF1\x41\x03\xC3\x45\x03\xDE\x48\x8D\x0C\x80\x41\x8B\x54\x88\x10\x41\x0F\x10\x0C\x88\x41\x0F\x11\x04\x88\x41\x8B\x42\x10\x41\x89\x44\x88\x10\x41\x0F\x11\x0A\x41\x89\x52\x10\x4D\x8D\x52\x14\x45\x3B\xD9\x72\x9C\xEB\x06\x8B\x45\xB3\x89\x45\x7F\x8B\xB7\x90\x00\x00\x00\x48\x03\xF3\x8B\x46\x0C\x85\xC0\x74\x7B\x8B\x7D\x7F\x8B\xC8\x48\x03\xCB\x41\xFF\xD4\x44\x8B\x3E\x4C\x8B\xE0\x44\x8B\x76\x10\x4C\x03\xFB\x4C\x03\xF3\x49\x8B\x0F\x48\x85\xC9\x74\x2D\x48\x8B\x7D\xBF\x79\x05\x0F\xB7\xD1\xEB\x07\x48\x8D\x51\x02\x48\x03\xD3\x49\x8B\xCC\xFF\xD7\x49\x83\xC7\x08\x49\x89\x06\x49\x83\xC6\x08\x49\x8B\x0F\x48\x85\xC9\x75\xDA\x8B\x7D\x7F\x45\x33\xFF\x44\x39\x7D\xB3\x74\x0F\x41\x83\xFD\x01\x76\x09\x69\xCF\xE8\x03\x00\x00\xFF\x55\xC7\x8B\x46\x20\x48\x83\xC6\x14\x4C\x8B\x65\xB7\x85\xC0\x75\x8C\x48\x8B\x7D\xCF\x4C\x8B\x6D\xBF\x44\x39\xBF\xF4\x00\x00\x00\x74\x68\x44\x8B\xB7\xF0\x00\x00\x00\x49\x83\xC6\x04\x4C\x03\xF3\xEB\x53\x41\x8B\x0E\x48\x03\xCB\x41\xFF\xD4\x41\x8B\x76\x08\x4C\x8B\xE0\x45\x8B\x7E\x0C\x48\x03\xF3\x4C\x03\xFB\xEB\x25\x49\x8B\x0F\x48\x85\xC9\x79\x05\x0F\xB7\xD1\xEB\x07\x48\x8D\x51\x02\x48\x03\xD3\x49\x8B\xCC\x41\xFF\xD5\x48\x89\x06\x48\x83\xC6\x08\x49\x83\xC7\x08\x33\xC0\x48\x39\x06\x75\xD4\x4C\x8B\x65\xB7\x49\x83\xC6\x20\x45\x33\xFF\x45\x39\x3E\x75\xA8\x45\x8B\xF7\x0F\xB7\x47\x14\x41\xBC\x01\x00\x00\x00\x66\x44\x3B\x7F\x06\x0F\x83\xCF\x00\x00\x00\x4C\x8B\x7D\xD7\x48\x8D\x77\x3C\x48\x03\xF0\x45\x33\xC9\x44\x39\x4E\xEC\x0F\x84\xA0\x00\x00\x00\x8B\x0E\x8B\xD1\xC1\xEA\x1E\x8B\xC1\x41\x23\xD4\xC1\xE8\x1D\xC1\xE9\x1F\x41\x23\xC4\x75\x24\x85\xD2\x75\x0E\xF7\xD9\x45\x1B\xC0\x41\x83\xE0\x07\x45\x03\xC4\xEB\x4F\xF7\xD9\xB8\x02\x00\x00\x00\x45\x1B\xC0\x44\x23\xC0\x44\x03\xC0\xEB\x3D\x85\xD2\x75\x20\x85\xC9\x75\x06\x44\x8D\x42\x10\xEB\x2F\x85\xD2\x75\x12\x85\xC9\x74\x08\x41\xB8\x80\x00\x00\x00\xEB\x1F\x44\x8B\x45\xAF\xEB\x1D\x85\xC9\x75\x06\x44\x8D\x41\x20\xEB\x0F\x44\x8B\x45\xAF\x85\xC9\xB8\x40\x00\x00\x00\x44\x0F\x45\xC0\x44\x89\x45\xAF\xF7\x06\x00\x00\x00\x04\x74\x09\x41\x0F\xBA\xE8\x09\x44\x89\x45\xAF\x8B\x4E\xE8\x4C\x8D\x4D\xAF\x8B\x56\xEC\x48\x03\xCB\x41\xFF\xD7\x45\x33\xC9\x0F\xB7\x47\x06\x45\x03\xF4\x48\x83\xC6\x28\x44\x3B\xF0\x0F\x82\x42\xFF\xFF\xFF\x45\x33\xFF\x45\x33\xC0\x33\xD2\x48\x83\xC9\xFF\xFF\x55\xDF\x44\x39\xBF\xD4\x00\x00\x00\x74\x24\x8B\x87\xD0\x00\x00\x00\x48\x8B\x74\x18\x18\xEB\x0F\x45\x33\xC0\x41\x8B\xD4\x48\x8B\xCB\xFF\xD0\x48\x8D\x76\x08\x48\x8B\x06\x48\x85\xC0\x75\xE9\x8B\x47\x28\x4D\x8B\xC4\x48\x03\xC3\x41\x8B\xD4\x48\x8B\xCB\xFF\xD0\x8B\x75\x67\x85\xF6\x0F\x84\x96\x00\x00\x00\x44\x39\xBF\x8C\x00\x00\x00\x0F\x84\x89\x00\x00\x00\x8B\x8F\x88\x00\x00\x00\x48\x03\xCB\x44\x8B\x59\x18\x45\x85\xDB\x74\x77\x44\x39\x79\x14\x74\x71\x44\x8B\x49\x20\x41\x8B\xFF\x8B\x51\x24\x4C\x03\xCB\x48\x03\xD3\x45\x85\xDB\x74\x5C\x45\x8B\x01\x45\x8B\xD7\x4C\x03\xC3\x74\x51\xEB\x10\x0F\xBE\xC0\x41\x03\xC2\x44\x8B\xD0\x41\xC1\xCA\x0D\x4D\x03\xC4\x41\x8A\x00\x84\xC0\x75\xE9\x41\x3B\xF2\x75\x05\x48\x85\xD2\x75\x16\xB8\x02\x00\x00\x00\x41\x03\xFC\x48\x03\xD0\x49\x83\xC1\x04\x41\x3B\xFB\x73\x1A\xEB\xBC\x8B\x49\x1C\x0F\xB7\x12\x48\x03\xCB\x8B\x04\x91\x8B\x55\x77\x48\x03\xC3\x48\x8B\x4D\x6F\xFF\xD0\x48\x8B\xC3\xEB\x02\x33\xC0\x48\x8B\x9C\x24\xD0\x00\x00\x00\x48\x81\xC4\x90\x00\x00\x00\x41\x5F\x41\x5E\x41\x5D\x41\x5C\x5F\x5E\x5D\xC3\xCC\xCC\x48\x89\x5C\x24\x08\x48\x89\x74\x24\x10\x57\x48\x83\xEC\x10\x65\x48\x8B\x04\x25\x60\x00\x00\x00\x8B\xF1\x48\x8B\x50\x18\x4C\x8B\x4A\x10\x4D\x8B\x41\x30\x4D\x85\xC0\x0F\x84\xB4\x00\x00\x00\x41\x0F\x10\x41\x58\x49\x63\x40\x3C\x33\xD2\x4D\x8B\x09\xF3\x0F\x7F\x04\x24\x42\x8B\x9C\x00\x88\x00\x00\x00\x85\xDB\x74\xD4\x48\x8B\x04\x24\x48\xC1\xE8\x10\x44\x0F\xB7\xD0\x45\x85\xD2\x74\x21\x48\x8B\x4C\x24\x08\x45\x8B\xDA\x0F\xBE\x01\xC1\xCA\x0D\x80\x39\x61\x7C\x03\x83\xC2\xE0\x03\xD0\x48\xFF\xC1\x49\x83\xEB\x01\x75\xE7\x4D\x8D\x14\x18\x33\xC9\x41\x8B\x7A\x20\x49\x03\xF8\x41\x39\x4A\x18\x76\x8F\x8B\x1F\x45\x33\xDB\x49\x03\xD8\x48\x8D\x7F\x04\x0F\xBE\x03\x48\xFF\xC3\x41\xC1\xCB\x0D\x44\x03\xD8\x80\x7B\xFF\x00\x75\xED\x41\x8D\x04\x13\x3B\xC6\x74\x0D\xFF\xC1\x41\x3B\x4A\x18\x72\xD1\xE9\x5B\xFF\xFF\xFF\x41\x8B\x42\x24\x03\xC9\x49\x03\xC0\x0F\xB7\x14\x01\x41\x8B\x4A\x1C\x49\x03\xC8\x8B\x04\x91\x49\x03\xC0\xEB\x02\x33\xC0\x48\x8B\x5C\x24\x20\x48\x8B\x74\x24\x28\x48\x83\xC4\x10\x5F\xC3'
    #MARKER:E
    
    if is64BitDLL(dllBytes):

        rdiShellcode = rdiShellcode64

        bootstrap = b''
        bootstrapSize = 64

        # call next instruction (Pushes next instruction address to stack)
        bootstrap += b'\xe8\x00\x00\x00\x00'

        # Set the offset to our DLL from pop result
        dllOffset = bootstrapSize - len(bootstrap) + len(rdiShellcode)

        # pop rcx - Capture our current location in memory
        bootstrap += b'\x59'

        # mov r8, rcx - copy our location in memory to r8 before we start modifying RCX
        bootstrap += b'\x49\x89\xc8'

        # add rcx, <Offset of the DLL>
        bootstrap += b'\x48\x81\xc1'
        bootstrap += pack('I', dllOffset)

        # mov edx, <Hash of function>
        bootstrap += b'\xba'
        bootstrap += pack('I', functionHash)

        # Setup the location of our user data
        # add r8, <Offset of the DLL> + <Length of DLL>
        bootstrap += b'\x49\x81\xc0'
        userDataLocation = dllOffset + len(dllBytes)
        bootstrap += pack('I', userDataLocation)

        # mov r9d, <Length of User Data>
        bootstrap += b'\x41\xb9'
        bootstrap += pack('I', len(userData))

        # push rsi - save original value
        bootstrap += b'\x56'

        # mov rsi, rsp - store our current stack pointer for later
        bootstrap += b'\x48\x89\xe6'

        # and rsp, 0x0FFFFFFFFFFFFFFF0 - Align the stack to 16 bytes
        bootstrap += b'\x48\x83\xe4\xf0'

        # sub rsp, 0x30 - Create some breathing room on the stack 
        bootstrap += b'\x48\x83\xec'
        bootstrap += b'\x30' # 32 bytes for shadow space + 8 bytes for last arg + 8 bytes for stack alignment

        # mov dword ptr [rsp + 0x20], <Flags> - Push arg 5 just above shadow space
        bootstrap += b'\xC7\x44\x24'
        bootstrap += b'\x20'
        bootstrap += pack('I', flags)

        # call - Transfer execution to the RDI
        bootstrap += b'\xe8'
        bootstrap += pack('b', bootstrapSize - len(bootstrap) - 4) # Skip over the remainder of instructions
        bootstrap += b'\x00\x00\x00'

        # mov rsp, rsi - Reset our original stack pointer
        bootstrap += b'\x48\x89\xf4'

        # pop rsi - Put things back where we left them
        bootstrap += b'\x5e'

        # ret - return to caller
        bootstrap += b'\xc3'

        if len(bootstrap) != bootstrapSize:
            raise Exception("x64 bootstrap length: {} != bootstrapSize: {}".format(len(bootstrap), bootstrapSize))

        # Ends up looking like this in memory:
        # Bootstrap shellcode
        # RDI shellcode
        # DLL bytes
        # User data
        return bootstrap + rdiShellcode + dllBytes + userData

    else: # 32 bit
        rdiShellcode = rdiShellcode32

        bootstrap = b''
        bootstrapSize = 46

        # call next instruction (Pushes next instruction address to stack)
        bootstrap += b'\xe8\x00\x00\x00\x00'

        # Set the offset to our DLL from pop result
        dllOffset = bootstrapSize - len(bootstrap) + len(rdiShellcode)

        # pop eax - Capture our current location in memory
        bootstrap += b'\x58'

        # push ebp
        bootstrap += b'\x55'

        # mov ebp, esp
        bootstrap += b'\x89\xe5'

        # mov ebx, eax - copy our location in memory to ebx before we start modifying eax
        bootstrap += b'\x89\xc3'

        # add eax, <Offset to the DLL>
        bootstrap += b'\x05'
        bootstrap += pack('I', dllOffset)

        # add ebx, <Offset to the DLL> + <Size of DLL>
        bootstrap += b'\x81\xc3'
        userDataLocation = dllOffset + len(dllBytes)
        bootstrap += pack('I', userDataLocation)

        # push <Flags>
        bootstrap += b'\x68'
        bootstrap += pack('I', flags)

        # push <Length of User Data>
        bootstrap += b'\x68'
        bootstrap += pack('I', len(userData))

        # push ebx
        bootstrap += b'\x53'

        # push <hash of function>
        bootstrap += b'\x68'
        bootstrap += pack('I', functionHash)

        # push eax
        bootstrap += b'\x50'

        # call - Transfer execution to the RDI
        bootstrap += b'\xe8'
        bootstrap += pack('b', bootstrapSize - len(bootstrap) - 4) # Skip over the remainder of instructions
        bootstrap += b'\x00\x00\x00'

        # leave
        bootstrap += b'\xc9'

        # ret - return to caller
        bootstrap += b'\xc3'

        if len(bootstrap) != bootstrapSize:
            raise Exception("x86 bootstrap length: {} != bootstrapSize: {}".format(len(bootstrap), bootstrapSize))

        # Ends up looking like this in memory:
        # Bootstrap shellcode
        # RDI shellcode
        # DLL bytes
        # User data
        return bootstrap + rdiShellcode + dllBytes + userData

    return False