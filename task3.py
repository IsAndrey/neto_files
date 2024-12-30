DATA = [
    'sorted/1.txt',
    'sorted/2.txt',
    'sorted/3.txt'
]


def sort_files(data, out='out.txt'):
    data_len = sorted(
        [
            [
                data.index(file_path),
                sum(1 for line in open(file_path, 'r', encoding='utf-8'))
            ]
            for file_path in data
        ],
        key=lambda x: x[1]
    )
    with open(out, 'w', encoding='utf-8') as f:
        for dl in data_len:
            f.writelines(
                [
                    data[dl[0]], '\n', str(dl[1]), '\n'
                ]
            )
            with open(data[dl[0]], 'r', encoding='utf-8') as fr:
                for line in fr:
                    f.write(line)

            if data_len.index(dl) < len(data_len)-1:
                f.write('\n')


if __name__ == '__main__':
    sort_files(DATA)
