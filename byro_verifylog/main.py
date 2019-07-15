import argparse
import sys
import json
import canonicaljson
import nacl.hash
import nacl.utils
import base64

PERSON_BYTES = b'byro logchain v1'

parser = argparse.ArgumentParser()
parser.add_argument('log_file', type=argparse.FileType('r'), default=sys.stdin, nargs='?')

class Verifier:
    def __init__(self):
        self.verified = {}
        self.invalid = []
        self.chains = {}

    def verify(self, json_input):
        for entry in json_input:
            if self.check_hash(entry):
                if entry['hash'] in self.verified:
                    self.invalid.append(
                        ['duplicate_hash', entry]
                    )
                else:
                    self.verified[entry['hash']] = entry
                    self.chains[entry['hash']] = entry['hash']

        chain_heads = {}
        chain_tails = {}

        for k, v in self.verified.items():
            head = k
            tail = v['entry']['prev_hash']

            if head in chain_tails:
                head = chain_tails.pop(head)

            if tail in chain_heads:
                tail = chain_heads.pop(tail)

            chain_heads[head] = tail
            chain_tails[tail] = head

        self.chains = chain_heads

    def print_report(self):
        print("Verified {} chains, {} invalid entries".format(len(self.chains), len(self.invalid)))
        print("Valid chains:")
        for head, tail in self.chains.items():
            print("\t{} -> {}".format(head, tail))


    @staticmethod
    def check_hash(entry):
        ad_encoded = canonicaljson.encode_canonical_json(entry['entry'])
        auth_hash = "blake2b:{}".format(
            nacl.hash.blake2b(ad_encoded, digest_size=64, person=PERSON_BYTES).decode(
                'us-ascii'
            )
        )

        if auth_hash != entry['hash']:
            return False

        # FIXME Handle case of data present or missing

        hdd_encoded = canonicaljson.encode_canonical_json(entry['data'])
        hdd_nonce = base64.b64decode(entry['entry']['auth_data']['nonce'])
        hdd_mac = nacl.hash.blake2b(hdd_encoded, digest_size=64, salt=hdd_nonce)

        hdd_hash = 'blake2b:{}'.format(hdd_mac.decode('us-ascii'))
        if hdd_hash != entry['entry']['auth_data']['data_mac']:
            return False

        return True


def main():
    args = parser.parse_args()
    json_input = json.load(args.log_file)
    v = Verifier()
    v.verify(json_input)
    v.print_report()


if __name__ == '__main__':
    main()
