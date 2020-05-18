import asyncio
import websockets
import json
import zlib
from pt.libs.utils import set_logging
import logging
from itertools import permutations
from optparse import OptionParser

set_logging(logging.DEBUG)

coin_pairs_base = [pair.upper().replace("_", "-") for pair in (
    "btc_usdt|ltc_usdt|eth_usdt|okb_usdt|etc_usdt|bch_usdt|eos_usdt|xrp_usdt|trx_usdt|bsv_usdt|dash_usdt|neo_usdt|qtum_usdt|xlm_usdt|ada_usdt|aac_usdt|abt_usdt|act_usdt|ae_usdt|algo_usdt|apm_usdt|ark_usdt|atom_usdt|bat_usdt|bcd_usdt|bec_usdt|bkx_usdt|bnt_usdt|btg_usdt|btm_usdt|btt_usdt|chat_usdt|cmt_usdt|cro_usdt|ctxc_usdt|cvc_usdt|cvt_usdt|dai_usdt|dcr_usdt|dgb_usdt|dgd_usdt|doge_usdt|ec_usdt|edo_usdt|egt_usdt|elf_usdt|fair_usdt|ftm_usdt|gas_usdt|gnt_usdt|gto_usdt|gusd_usdt|hbar_usdt|hc_usdt|hdao_usdt|hpb_usdt|hyc_usdt|icx_usdt|int_usdt|iost_usdt|iota_usdt|itc_usdt|kan_usdt|kcash_usdt|knc_usdt|lamb_usdt|lba_usdt|leo_usdt|let_usdt|link_usdt|lrc_usdt|lsk_usdt|mana_usdt|mco_usdt|mdt_usdt|mith_usdt|mkr_usdt|mof_usdt|nano_usdt|nas_usdt|nuls_usdt|omg_usdt|ont_usdt|orbs_usdt|ors_usdt|pax_usdt|pay_usdt|ppt_usdt|pst_usdt|qun_usdt|r_usdt|rfr_usdt|rnt_usdt|road_usdt|rvn_usdt|sc_usdt|snt_usdt|soc_usdt|storj_usdt|swftc_usdt|tct_usdt|theta_usdt|topc_usdt|trio_usdt|true_usdt|tusd_usdt|usdc_usdt|vib_usdt|vnt_usdt|vsys_usdt|waves_usdt|wtc_usdt|wxt_usdt|xem_usdt|xmr_usdt|xtz_usdt|xuc_usdt|yee_usdt|you_usdt|zec_usdt|zen_usdt|zil_usdt|zip_usdt|zrx_usdt|ltc_okb|etc_okb|eos_okb|xrp_okb|trx_okb|dash_okb|neo_okb|ae_okb|egt_okb|iota_okb|sc_okb|wxt_okb|zec_okb|ltc_btc|eth_btc|okb_btc|etc_btc|bch_btc|eos_btc|xrp_btc|trx_btc|bsv_btc|dash_btc|neo_btc|qtum_btc|xlm_btc|ada_btc|aac_btc|abt_btc|act_btc|ae_btc|algo_btc|apm_btc|ardr_btc|ark_btc|atom_btc|bat_btc|bcd_btc|bec_btc|bkx_btc|bnt_btc|btg_btc|btm_btc|btt_btc|chat_btc|cmt_btc|cro_btc|ctxc_btc|cvc_btc|cvt_btc|dcr_btc|dgb_btc|dgd_btc|edo_btc|egt_btc|elf_btc|gas_btc|gnt_btc|gnx_btc|gto_btc|gusd_btc|hbar_btc|hc_btc|hpb_btc|hyc_btc|icx_btc|int_btc|iost_btc|iota_btc|itc_btc|kan_btc|kcash_btc|knc_btc|lba_btc|leo_btc|let_btc|link_btc|lrc_btc|lsk_btc|mana_btc|mco_btc|mdt_btc|mith_btc|mkr_btc|mof_btc|nano_btc|nas_btc|nuls_btc|nxt_btc|omg_btc|ont_btc|ors_btc|pax_btc|pay_btc|pma_btc|pst_btc|qun_btc|r_btc|rfr_btc|rvn_btc|sbtc_btc|sc_btc|snc_btc|snt_btc|soc_btc|spnd_btc|swftc_btc|tct_btc|theta_btc|trio_btc|true_btc|tusd_btc|usdc_btc|vib_btc|vite_btc|vsys_btc|waves_btc|wtc_btc|wxt_btc|xem_btc|xmr_btc|xtz_btc|you_btc|zec_btc|zen_btc|zil_btc|zip_btc|zrx_btc|ltc_eth|okb_eth|etc_eth|eos_eth|xrp_eth|trx_eth|dash_eth|neo_eth|qtum_eth|xlm_eth|ada_eth|aac_eth|abt_eth|ae_eth|algo_eth|atom_eth|auto_eth|btm_eth|btt_eth|cmt_eth|ctxc_eth|cvc_eth|dcr_eth|dgd_eth|egt_eth|elf_eth|fair_eth|gas_eth|gnx_eth|gto_eth|hc_eth|hpb_eth|hyc_eth|int_eth|iost_eth|iota_eth|kan_eth|kcash_eth|leo_eth|link_eth|lrc_eth|mana_eth|mco_eth|mdt_eth|mith_eth|mkr_eth|mof_eth|nano_eth|nas_eth|nuls_eth|omg_eth|ont_eth|ors_eth|sc_eth|storj_eth|swftc_eth|topc_eth|trio_eth|true_eth|waves_eth|wtc_eth|xem_eth|xmr_eth|you_eth|zec_eth|zen_eth|zil_eth|zrx_eth|btc_dai|eth_dai"
).split("|")]

coins = [coin.upper() for coin in list(set((
                                               "btc_usdt|ltc_usdt|eth_usdt|okb_usdt|etc_usdt|bch_usdt|eos_usdt|xrp_usdt|trx_usdt|bsv_usdt|dash_usdt|neo_usdt|qtum_usdt|xlm_usdt|ada_usdt|aac_usdt|abt_usdt|act_usdt|ae_usdt|algo_usdt|apm_usdt|ark_usdt|atom_usdt|bat_usdt|bcd_usdt|bec_usdt|bkx_usdt|bnt_usdt|btg_usdt|btm_usdt|btt_usdt|chat_usdt|cmt_usdt|cro_usdt|ctxc_usdt|cvc_usdt|cvt_usdt|dai_usdt|dcr_usdt|dgb_usdt|dgd_usdt|doge_usdt|ec_usdt|edo_usdt|egt_usdt|elf_usdt|fair_usdt|ftm_usdt|gas_usdt|gnt_usdt|gto_usdt|gusd_usdt|hbar_usdt|hc_usdt|hdao_usdt|hpb_usdt|hyc_usdt|icx_usdt|int_usdt|iost_usdt|iota_usdt|itc_usdt|kan_usdt|kcash_usdt|knc_usdt|lamb_usdt|lba_usdt|leo_usdt|let_usdt|link_usdt|lrc_usdt|lsk_usdt|mana_usdt|mco_usdt|mdt_usdt|mith_usdt|mkr_usdt|mof_usdt|nano_usdt|nas_usdt|nuls_usdt|omg_usdt|ont_usdt|orbs_usdt|ors_usdt|pax_usdt|pay_usdt|ppt_usdt|pst_usdt|qun_usdt|r_usdt|rfr_usdt|rnt_usdt|road_usdt|rvn_usdt|sc_usdt|snt_usdt|soc_usdt|storj_usdt|swftc_usdt|tct_usdt|theta_usdt|topc_usdt|trio_usdt|true_usdt|tusd_usdt|usdc_usdt|vib_usdt|vnt_usdt|vsys_usdt|waves_usdt|wtc_usdt|wxt_usdt|xem_usdt|xmr_usdt|xtz_usdt|xuc_usdt|yee_usdt|you_usdt|zec_usdt|zen_usdt|zil_usdt|zip_usdt|zrx_usdt|ltc_okb|etc_okb|eos_okb|xrp_okb|trx_okb|dash_okb|neo_okb|ae_okb|egt_okb|iota_okb|sc_okb|wxt_okb|zec_okb|ltc_btc|eth_btc|okb_btc|etc_btc|bch_btc|eos_btc|xrp_btc|trx_btc|bsv_btc|dash_btc|neo_btc|qtum_btc|xlm_btc|ada_btc|aac_btc|abt_btc|act_btc|ae_btc|algo_btc|apm_btc|ardr_btc|ark_btc|atom_btc|bat_btc|bcd_btc|bec_btc|bkx_btc|bnt_btc|btg_btc|btm_btc|btt_btc|chat_btc|cmt_btc|cro_btc|ctxc_btc|cvc_btc|cvt_btc|dcr_btc|dgb_btc|dgd_btc|edo_btc|egt_btc|elf_btc|gas_btc|gnt_btc|gnx_btc|gto_btc|gusd_btc|hbar_btc|hc_btc|hpb_btc|hyc_btc|icx_btc|int_btc|iost_btc|iota_btc|itc_btc|kan_btc|kcash_btc|knc_btc|lba_btc|leo_btc|let_btc|link_btc|lrc_btc|lsk_btc|mana_btc|mco_btc|mdt_btc|mith_btc|mkr_btc|mof_btc|nano_btc|nas_btc|nuls_btc|nxt_btc|omg_btc|ont_btc|ors_btc|pax_btc|pay_btc|pma_btc|pst_btc|qun_btc|r_btc|rfr_btc|rvn_btc|sbtc_btc|sc_btc|snc_btc|snt_btc|soc_btc|spnd_btc|swftc_btc|tct_btc|theta_btc|trio_btc|true_btc|tusd_btc|usdc_btc|vib_btc|vite_btc|vsys_btc|waves_btc|wtc_btc|wxt_btc|xem_btc|xmr_btc|xtz_btc|you_btc|zec_btc|zen_btc|zil_btc|zip_btc|zrx_btc|ltc_eth|okb_eth|etc_eth|eos_eth|xrp_eth|trx_eth|dash_eth|neo_eth|qtum_eth|xlm_eth|ada_eth|aac_eth|abt_eth|ae_eth|algo_eth|atom_eth|auto_eth|btm_eth|btt_eth|cmt_eth|ctxc_eth|cvc_eth|dcr_eth|dgd_eth|egt_eth|elf_eth|fair_eth|gas_eth|gnx_eth|gto_eth|hc_eth|hpb_eth|hyc_eth|int_eth|iost_eth|iota_eth|kan_eth|kcash_eth|leo_eth|link_eth|lrc_eth|mana_eth|mco_eth|mdt_eth|mith_eth|mkr_eth|mof_eth|nano_eth|nas_eth|nuls_eth|omg_eth|ont_eth|ors_eth|sc_eth|storj_eth|swftc_eth|topc_eth|trio_eth|true_eth|waves_eth|wtc_eth|xem_eth|xmr_eth|you_eth|zec_eth|zen_eth|zil_eth|zrx_eth|btc_dai|eth_dai"
                                           ).replace("_", "|").split("|")))]

global_vars = dict()
coin_pairs_object = dict()
pairs = []
combos = []
for pair in coin_pairs_base:
    coin_pairs_object[pair] = pair
    coin_pairs_object[pair.split("-")[1] + "-" + pair.split("-")[0]] = pair

price_base = 100
exchange_fee = 1 - 0.0015


def handle_result(combo):
    global global_vars
    r = dict()
    r["combo"] = combo
    r["pairs"] = [
        "{}-{}".format(combo[0], combo[1]),
        "{}-{}".format(combo[1], combo[2]),
        "{}-{}".format(combo[2], combo[0])
    ]
    try:
        r["pairs_fetch"] = [
            coin_pairs_object[r["pairs"][0]],
            coin_pairs_object[r["pairs"][1]],
            coin_pairs_object[r["pairs"][2]],
        ]
    except Exception as e:
        return None

    j = 0
    for i in r["pairs_fetch"]:
        if i in global_vars.keys():
            j += 1
    if j < 3:
        return

    r["fee"] = [
        float(global_vars[r["pairs_fetch"][0]]),
        float(global_vars[r["pairs_fetch"][1]]),
        float(global_vars[r["pairs_fetch"][2]])
    ]

    r['price_base'] = price_base
    r['exchange_fee'] = exchange_fee
    r['price'] = []

    if r["pairs_fetch"][0] == r["pairs"][0]:
        r['price'].append(r['exchange_fee'] * r['price_base'] * r["fee"][0])
    else:
        r['price'].append(r['exchange_fee'] * r['price_base'] / r["fee"][0])

    if r["pairs_fetch"][1] == r["pairs"][1]:
        r['price'].append(r['exchange_fee'] * r['price'][0] * r["fee"][1])
    else:
        r['price'].append(r['exchange_fee'] * r['price'][0] / r["fee"][1])

    if r["pairs_fetch"][2] == r["pairs"][2]:
        r['price'].append(r['exchange_fee'] * r['price'][1] * r["fee"][2])
    else:
        r['price'].append(r['exchange_fee'] * r['price'][1] / r["fee"][2])
    r['price_diff'] = r['price'][2] - r['price_base']
    return r


async def handle_combos():
    while 1:
        for item in combos:
            logging.info(item)
            r1 = handle_result(item)
            r2 = handle_result([item[0], item[1], item[2]])
            # print(r1)
            if r2 is not None and (r1['price_diff'] > 0 or r2['price_diff'] > 0):
                logging.info("%s: %f, %s: %f,",
                             "->".join(r1["combo"]), r1['price_diff'],
                             "->".join(r2["combo"]), r2['price_diff'])
            else:
                if r2 is not None:
                    logging.info("%s: %f, %s: %f,",
                                 "->".join(r1["combo"]), r1['price_diff'],
                                 "->".join(r2["combo"]), r2['price_diff'])
        await asyncio.sleep(1)


async def handle_msg(websocket):
    while True:
        recv_text = await websocket.recv()
        data = pako_inflate_raw(recv_text)
        data = json.loads(data)
        # logging.error(data)
        if "errorCode" in data.keys() and data['errorCode'] > 0:
            logging.error(data['message'])
        else:
            if "data" in data.keys():
                global_vars[data['data'][0]['instrument_id']] = data['data'][0]['last']
                logging.info("%s %s", data['data'][0]['instrument_id'], data['data'][0]['last'])
                logging.info(global_vars.keys())

def pako_inflate_raw(data):
    decompress = zlib.decompressobj(-15)
    decompressed_data = decompress.decompress(data)
    decompressed_data += decompress.flush()
    return decompressed_data


async def main_logic(i):
    async with websockets.connect('wss://okexcomreal.bafang.com:8443/ws/v3') as websocket:
        for pair in pairs[i]:
            await websocket.send(json.dumps(dict(
                op="subscribe",
                args=["spot/ticker:" + pair],
            )))
        await handle_msg(websocket)


def all_run():
    a = 1
    b = 5

    combos = []
    k = 0
    coins = []
    for i in range(b):
        row = []
        for j in range(a):
            pair = coin_pairs_base[k]
            if pair.split("-")[0] not in coins:
                coins.append(pair.split("-")[0])
            if pair.split("-")[1] not in coins:
                coins.append(pair.split("-")[1])
            row.append(pair)
            k += 1
        pairs.append(row)

    # coins = ["USDT", "BTC", "OKB", "ETC", "ETH", "BCH", "LINK"]
    for item in permutations(coins, 3):
        if item[0] != "USDT":
            continue
        i = 0
        if "{}-{}".format(item[0], item[1]) in coin_pairs_object.keys():
            i += 1
        if "{}-{}".format(item[1], item[2]) in coin_pairs_object.keys():
            i += 1
        if "{}-{}".format(item[2], item[0]) in coin_pairs_object.keys():
            i += 1
        j = 0
        if "{}-{}".format(item[0], item[2]) in coin_pairs_object.keys():
            j += 1
        if "{}-{}".format(item[2], item[1]) in coin_pairs_object.keys():
            j += 1
        if "{}-{}".format(item[1], item[0]) in coin_pairs_object.keys():
            j += 1
        if i + j == 6:
            combos.append(item)


def single_run(combo,boot,workers,subscribes):
    coins = combo.split("|")
    pairs_ = []
    for item in permutations(coins, 3):
        if item[0] != boot.upper():
            continue
        i = 0
        pair_1 = "{}-{}".format(item[0], item[1])
        if pair_1 in coin_pairs_object.keys():
            i += 1

        pair_2 = "{}-{}".format(item[1], item[2])
        if pair_2 in coin_pairs_object.keys():
            i += 1
        pair_3 = "{}-{}".format(item[2], item[0])
        if pair_3 in coin_pairs_object.keys():
            i += 1
        j = 0
        pair_4 = "{}-{}".format(item[0], item[2])
        if pair_4 in coin_pairs_object.keys():
            j += 1
        pair_5 = "{}-{}".format(item[2], item[1])
        if pair_5 in coin_pairs_object.keys():
            j += 1
        pair_6 = "{}-{}".format(item[1], item[0])
        if pair_6 in coin_pairs_object.keys():
            j += 1

        if i + j == 6:
            if pair_1 in coin_pairs_base and pair_1 not in pairs_:
                pairs_.append(pair_1)
            if pair_2 in coin_pairs_base and pair_2 not in pairs_:
                pairs_.append(pair_2)
            if pair_3 in coin_pairs_base and pair_3 not in pairs_:
                pairs_.append(pair_3)
            if pair_4 in coin_pairs_base and pair_4 not in pairs_:
                pairs_.append(pair_4)
            if pair_5 in coin_pairs_base and pair_5 not in pairs_:
                pairs_.append(pair_5)
            if pair_6 in coin_pairs_base and pair_6 not in pairs_:
                pairs_.append(pair_6)
            combos.append(item)

    k = 0
    for i in range(workers):
        row = []
        for j in range(subscribes):
            if k == len(pairs_):
                continue
            pair = pairs_[k]
            row.append(pair)
            k += 1
        if len(row) > 0:
            pairs.append(row)



if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option("-c", "--combo", dest="combo",
                      help="货币组合: BTC|ETH|OKB|LINK|USDT")

    parser.add_option("-b", "--boot", dest="boot",
                      help="起始货币: USDT")

    parser.add_option("-w", "--workers", dest="workers", default=False,
                      help="工作者数量")

    parser.add_option("-s", "--subscribes", dest="subscribes", default=False,
                      help="每个工作者处理数量")


    (options, args) = parser.parse_args()
    combo = options.combo
    boot = options.boot
    workers = options.workers
    subscribes = options.subscribes

    logging.info(options)
    pass
    workers = int(workers)
    subscribes = int(subscribes)
    single_run(combo, boot,workers,subscribes)

    logging.info("=====>>>>>>>>")
    logging.info("combos: %s", combos)
    logging.info("pairs: %s", pairs)

    if len(pairs) > 0:
        loop = asyncio.get_event_loop()
        tasks = []
        for i in range(workers):
            task = asyncio.ensure_future(main_logic(i))
            tasks.append(task)
        tasks.append(asyncio.ensure_future(handle_combos()))
        loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()
