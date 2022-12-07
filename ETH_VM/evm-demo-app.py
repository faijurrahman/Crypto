# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



# python3 -m pip install py-evm
# Or get source code from here: git clone --recursive https://github.com/ethereum/py-evm.git
# Also for more details document of py-evm please check here: https://py-evm.readthedocs.io/en/latest/guides/quickstart.html





# Details document here: https://py-evm.readthedocs.io/en/latest/cookbook/index.html
def use_EVM_Chain_Object():
    import inspect
    print("\nFunction:", inspect.stack()[0][3])

    from eth import constants, Chain
    from eth.vm.forks.frontier import FrontierVM
    from eth.vm.forks.homestead import HomesteadVM
    from eth.chains.mainnet import HOMESTEAD_MAINNET_BLOCK
    from eth.db.atomic import AtomicDB
    from eth.chains.mainnet import MAINNET_GENESIS_HEADER

    chain_class = Chain.configure(
        __name__='Test Chain',
        vm_configuration=(
            (constants.GENESIS_BLOCK_NUMBER, FrontierVM),
            (HOMESTEAD_MAINNET_BLOCK, HomesteadVM),
        ),
    )

    # initialize a fresh chain
    chain = chain_class.from_genesis_header(AtomicDB(), MAINNET_GENESIS_HEADER)






# Details document here: https://py-evm.readthedocs.io/en/latest/cookbook/index.html
def creating_Custom_State_And_Balance():
    import inspect
    print("\nFunction:", inspect.stack()[0][3])

    from eth_keys import keys
    from eth import constants
    from eth.chains.mainnet import MainnetChain
    from eth.db.atomic import AtomicDB
    from eth_utils import to_wei, encode_hex

    # Giving funds to some address
    SOME_ADDRESS = b'\x85\x82\xa2\x89V\xb9%\x93M\x03\xdd\xb4Xu\xe1\x8e\x85\x93\x12\xc1'
    GENESIS_STATE = {
        SOME_ADDRESS: {
            "balance": to_wei(10000, 'ether'),
            "nonce": 0,
            "code": b'',
            "storage": {}
        }
    }

    GENESIS_PARAMS = {
        'difficulty': constants.GENESIS_DIFFICULTY,
    }

    chain = MainnetChain.from_genesis(AtomicDB(), GENESIS_PARAMS, GENESIS_STATE)
    current_vm = chain.get_vm()
    state = current_vm.state
    balance = state.get_balance(SOME_ADDRESS)
    print("Balance:", balance)







# Details document here: https://py-evm.readthedocs.io/en/latest/guides/building_an_app_that_uses_pyevm.html
def create_Mock_Address_And_Balance():
    import inspect
    print("\nFunction:", inspect.stack()[0][3])

    from eth import constants
    from eth.chains.mainnet import MainnetChain
    from eth.db.atomic import AtomicDB
    from eth_utils import to_wei, encode_hex

    MOCK_ADDRESS = constants.ZERO_ADDRESS
    DEFAULT_INITIAL_BALANCE = to_wei(10000, 'ether')

    GENESIS_PARAMS = {
        'difficulty': constants.GENESIS_DIFFICULTY,
    }
    GENESIS_STATE = {
        MOCK_ADDRESS: {
            "balance": DEFAULT_INITIAL_BALANCE,
            "nonce": 0,
            "code": b'',
            "storage": {}
        }
    }

    chain = MainnetChain.from_genesis(AtomicDB(), GENESIS_PARAMS, GENESIS_STATE)
    mock_address_balance = chain.get_vm().state.get_balance(MOCK_ADDRESS)
    print("The balance of address {} is {} wei".format(
        encode_hex(MOCK_ADDRESS),
        mock_address_balance)
    )





# Details document here: https://py-evm.readthedocs.io/en/latest/guides/understanding_the_mining_process.html
def mine_First_Block():
    import inspect
    print("\nFunction:", inspect.stack()[0][3])

    from eth import constants
    from eth.chains.base import MiningChain
    from eth.vm.forks.byzantium import ByzantiumVM
    from eth.db.atomic import AtomicDB
    from eth.consensus.pow import mine_pow_nonce

    GENESIS_PARAMS = {
        'difficulty': 1,
        'gas_limit': 3141592,
        'timestamp': 1514764800,
    }
    klass = MiningChain.configure(
        __name__='TestChain',
        vm_configuration=(
            (constants.GENESIS_BLOCK_NUMBER, ByzantiumVM),
        ))
    chain = klass.from_genesis(AtomicDB(), GENESIS_PARAMS)

    # We have to finalize the block first in order to be able read the
    # attributes that are important for the PoW algorithm
    block_result = chain.get_vm().finalize_block(chain.get_block())
    block = block_result.block

    # based on mining_hash, block number and difficulty we can perform
    # the actual Proof of Work (PoW) mechanism to mine the correct
    # nonce and mix_hash for this block
    nonce, mix_hash = mine_pow_nonce(
        block.number,
        block.header.mining_hash,
        block.header.difficulty)

    block = chain.mine_block(mix_hash=mix_hash, nonce=nonce)
    print(block)





# Details document here: https://py-evm.readthedocs.io/en/latest/guides/understanding_the_mining_process.html
def mine_First_Block_With_Transaction():
    import inspect
    print("\nFunction:", inspect.stack()[0][3])

    from eth_keys import keys
    from eth_utils import decode_hex
    from eth_typing import Address
    from eth import constants
    from eth.chains.base import MiningChain
    from eth.consensus.pow import mine_pow_nonce
    from eth.vm.forks.byzantium import ByzantiumVM
    from eth.db.atomic import AtomicDB

    GENESIS_PARAMS = {
        'difficulty': 1,
        'gas_limit': 3141592,
        # We set the timestamp, just to make this documented example reproducible.
        # In common usage, we remove the field to let py-evm choose a reasonable default.
        'timestamp': 1514764800,
    }

    SENDER_PRIVATE_KEY = keys.PrivateKey(
        decode_hex('0x45a915e4d060149eb4365960e6a7a45f334393093061116b197e3240065ff2d8')
    )

    SENDER = Address(SENDER_PRIVATE_KEY.public_key.to_canonical_address())
    RECEIVER = Address(b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x02')

    klass = MiningChain.configure(
        __name__='TestChain',
        vm_configuration=(
            (constants.GENESIS_BLOCK_NUMBER, ByzantiumVM),
        ))

    chain = klass.from_genesis(AtomicDB(), GENESIS_PARAMS)
    genesis = chain.get_canonical_block_header_by_number(0)
    vm = chain.get_vm()

    nonce = vm.state.get_nonce(SENDER)
    tx = vm.create_unsigned_transaction(
        nonce=nonce,
        gas_price=0,
        gas=100000,
        to=RECEIVER,
        value=0,
        data=b'',
    )

    signed_tx = tx.as_signed_transaction(SENDER_PRIVATE_KEY)

    chain.apply_transaction(signed_tx)

    # Normally, we can let the timestamp be chosen automatically, but
    # for the sake of reproducing exactly the same block every time,
    # we will set it manually here:
    chain.set_header_timestamp(genesis.timestamp + 1)

    # We have to finalize the block first in order to be able read the
    # attributes that are important for the PoW algorithm
    block_result = chain.get_vm().finalize_block(chain.get_block())
    block = block_result.block

    # based on mining_hash, block number and difficulty we can perform
    # the actual Proof of Work (PoW) mechanism to mine the correct
    # nonce and mix_hash for this block
    nonce, mix_hash = mine_pow_nonce(
        block.number,
        block.header.mining_hash,
        block.header.difficulty
    )

    chain.mine_block(mix_hash=mix_hash, nonce=nonce)
    #< ByzantiumBlock(
    # Block #1-0xe372..385c)>





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    use_EVM_Chain_Object()
    creating_Custom_State_And_Balance()
    create_Mock_Address_And_Balance()
    #mine_First_Block() #There is an issue in this fuction
    mine_First_Block_With_Transaction()


