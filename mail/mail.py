import re


class Mail:
    def __init__(self, delivery_id: str, address: str, local_remote: str):
        self.id = delivery_id.replace(':', '')
        self.state = ''
        self.ip = '' if local_remote == 'remote' else '127.0.0.1'
        self.address = address.strip()

    def __str__(self):
        return f'id {self.id} {self.state} {self.ip} {self.address}'


def read_mails() -> dict[str, Mail]:
    result = {}
    with open('maillog.txt', 'r') as f:
        for line in f.readlines():
            if line.__contains__('starting delivery'):
                _, _, _, delivery_id, _, message_id, _, local_remote, address = line.split(' ')
                result[delivery_id] = Mail(delivery_id, address, local_remote)
            elif line.__contains__('delivery'):
                _, _, delivery_id, state, info = line.split(' ')
                if delivery_id in result:
                    result[delivery_id].state = state.replace(':', '')
                    result[delivery_id].ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', info)
    return result


if __name__ == "__main__":
    # 把id、状态、IP地址和目标邮箱提取出来
    mails = read_mails()
    list(map(print, mails.values()))

    # 统计出现错误最多的是那种邮箱
    hosts = {}
    for host_name in [mail.address.split('@')[1] for _, mail in mails.items() if mail.state == 'failure']:
        hosts[host_name] = hosts.get(host_name, 0) + 1
    hosts = sorted(hosts.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    max_count = hosts[0][1]
    print('\n\nthe most failure host is: ')
    print([host[0] for host in hosts if host[1] >= max_count])
