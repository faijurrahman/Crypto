# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


#python3 -m pip install bitcoinlib
def create_BitcoinLib_Wallet():
    from bitcoinlib.wallets import Wallet
    mnemonic = "hotel laptop random problem corn nut fun happy maximum federal wrap address"
    w = Wallet.create('Wallet1', keys=mnemonic, network='bitcoin')
    k = w.key_for_path([0, 0])
    print("default:", k.address)
    k = w.key_for_path([0, 1])
    print("Path: [0,1]", k.address)

#Source: https://pypi.org/project/pywallet/
#python3 -m pip install pywallet
def create_BIP32_PyWallet():
    from pywallet import wallet

    # generate 12 word mnemonic seed
    seed = wallet.generate_mnemonic()

    # create bitcoin wallet
    w = wallet.create_wallet(network="BTC", seed=seed, children=1)
    print(w)

    # create ethereum wallet
    w = wallet.create_wallet(network="ETH", seed=seed, children=1)
    print(w)

    #Generate wallet from public key
    WALLET_PUBKEY = 'YOUR WALLET XPUB'
    # generate address for specific user (id = 10)
    user_addr = wallet.create_address(network="BTC", xpub=WALLET_PUBKEY, child=10)
    # or generate a random address, based on timestamp
    rand_addr = wallet.create_address(network="BTC", xpub=WALLET_PUBKEY)
    print("User Address\n", user_addr)
    print("Random Address\n", rand_addr)



#Source: https: // github.com / meherett / python - hdwallet
#python3 -m pip install hdwallet
def create_Ethereum_BIP44_HDWallet():
    from hdwallet import BIP44HDWallet
    from hdwallet.cryptocurrencies import EthereumMainnet
    from hdwallet.derivations import BIP44Derivation
    from hdwallet.utils import generate_mnemonic
    from typing import Optional

    # Generate english mnemonic words
    MNEMONIC: str = generate_mnemonic(language="english", strength=128)
    # Secret passphrase/password for mnemonic
    PASSPHRASE: Optional[str] = None  # "meherett"

    # Initialize Ethereum mainnet BIP44HDWallet
    bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
    # Get Ethereum BIP44HDWallet from mnemonic
    bip44_hdwallet.from_mnemonic(
        mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE
    )
    # Clean default BIP44 derivation indexes/paths
    bip44_hdwallet.clean_derivation()

    print("Mnemonic:", bip44_hdwallet.mnemonic())
    print("Base HD Path:  m/44'/60'/0'/0/{address_index}", "\n")

    # Get Ethereum BIP44HDWallet information's from address index
    for address_index in range(10):
        # Derivation from Ethereum BIP44 derivation path
        bip44_derivation: BIP44Derivation = BIP44Derivation(
            cryptocurrency=EthereumMainnet, account=0, change=False, address=address_index
        )
        # Drive Ethereum BIP44HDWallet
        bip44_hdwallet.from_path(path=bip44_derivation)
        # Print address_index, path, address and private_key
        # m / purpose' / coin_type' / account' / change / address_index (Check here: https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki)
        print(f"({address_index}) {bip44_hdwallet.path()} {bip44_hdwallet.address()} 0x{bip44_hdwallet.private_key()}")
        # Clean derivation indexes/paths
        bip44_hdwallet.clean_derivation()




#Source: https: // github.com / meherett / python - hdwallet
#python3 -m pip install hdwallet
def create_BITCOIN_BIP44_HDWallet():
    from hdwallet import HDWallet
    from hdwallet.utils import generate_entropy
    from hdwallet.symbols import BTC as SYMBOL
    from typing import Optional

    import json

    # Choose strength 128, 160, 192, 224 or 256
    STRENGTH: int = 160  # Default is 128
    # Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese or korean
    LANGUAGE: str = "english"  # Default is english
    # Generate new entropy hex string
    ENTROPY: str = generate_entropy(strength=STRENGTH)
    # Secret passphrase for mnemonic
    PASSPHRASE: Optional[str] = None  # "meherett"

    # Initialize Bitcoin mainnet HDWallet
    hdwallet: HDWallet = HDWallet(symbol=SYMBOL, use_default_path=False)
    # Get Bitcoin HDWallet from entropy
    hdwallet.from_entropy(
        entropy=ENTROPY, language=LANGUAGE, passphrase=PASSPHRASE
    )

    # Derivation from path
    # hdwallet.from_path("m/44'/0'/0'/0/0")
    # Or derivation from index
    hdwallet.from_index(44, hardened=True)
    hdwallet.from_index(0, hardened=True)
    hdwallet.from_index(0, hardened=True)
    hdwallet.from_index(0)
    hdwallet.from_index(0)

    # Print all Bitcoin HDWallet information's
    print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))

#Source: https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md
def print_WordList_BIP39_HDWallet():
    wordlist = open('HDWallet_BIP39_Word_List_English.txt', 'r')
    print("BIP39: List of 2048 English Words:")
    index = 0
    for word in wordlist.readlines():
        index += 1
        print(index, ":", word.strip())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # !/usr/bin/env python3

    # Check document of BIP32 (HDWallet), BIP39 (2048 wordlist), BIP44 (Hirarchical HDWallet)
    # More details here: https://github.com/bitcoin/bips

    #Step-by-Step explanation: https://medium.com/cosmostation/the-magic-behind-a-mnemonic-phrase-and-hd-wallets-let-us-explain-43d9c97f6098

    print_WordList_BIP39_HDWallet()
    #create_BitcoinLib_Wallet() #Using Bitcoin Library. Note: not robust code
    #create_BIP32_PyWallet() #Using PyWallet. Note: Broken PyWallet library
    create_Ethereum_BIP44_HDWallet() #Using HDWallet Library
    create_BITCOIN_BIP44_HDWallet() #Using HDWallet Library



