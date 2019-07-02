import opcua

url = "opc.tcp://127.0.0.1:4840"

if __name__ == "__main__":

    client = opcua.Client(url)
    try:
        client.connect()
        root = client.get_root_node()
        print("Objects node is: ", root)
        children = root.get_children()
        print("Children of root are: ", children)

        for ch in children:
            print("------------------------------------")
            print("nodeID: ", ch.nodeid)
            print("browse_name: ", ch.get_browse_name())
            for lch in ch.get_children():
                print(ch, " browse_name: ", ch.get_browse_name())
            print("------------------------------------")

    finally:
        client.disconnect()
