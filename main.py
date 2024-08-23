from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)

# Client to connect to localnet
algorand = AlgorandClient.default_local_net()

# Import dispenser from KMD
dispenser = algorand.account.dispenser()
#print("Dispenser Address", dispenser.address)

creator = algorand.account.random()
# print("Creator Address", creator.address)
# print(algorand.account.get_information(creator.address))


algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )
)

print(algorand.account.get_information(creator.address))

# create a custom ASA token
sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=100,
        asset_name="Edu4Teen",
        unit_name="E4T",
    )
)

asset_id=sent_txn["confirmation"]["asset-index"]
print("Asset ID", asset_id)


receiver_acct = algorand.account.random()

algorand.send.paymentalgorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=receiver_acct.address,
        amount=10_000_000
    )
)

print(algorand.account.get_information(receiver_acct.address))

asset_transfer = algorand.send.asset_transfer(
    sender=creator.address,
    receiver=receiver_acct.address,
    asset_id=asset_id,
    amount=10
)

#create a group txn
group_txn = algorand.new_group()

group_txn.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver_acct.address,
        asset_id=asset_id,
    )
)

group_txn.add_payment(
    PayParams(
        sender=receiver_acct.address,
        receiver=creator.address,
        amount=1_100_100 # 1 algo
    )
)

group_txn.add_asset_transfer(
    sender=creator.address,
    receiver=receiver_acct.address,
    asset_id=asset_id,
    amount=10
)

group_txn.execute()

print("Receiver account asset Balance", algorand.account.get_information(receiver_acct)['assets'][0]['amount'])

