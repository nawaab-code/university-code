# University code

Course exercises organized by semester and course. Each CY52 networking experiment has its own folder, runnable Python code, and a question-specific README.

## Repository map

| Course | Contents | Requirements |
| --- | --- | --- |
| [Semester 4 / CYL46](Semester%204/CYL46) | `1.sql`: MySQL library database schema, sample data, and queries | MySQL |
| [Semester 4 / CYL48](Semester%204/CYL48) | `1.py`–`8.py`: NumPy, pandas, Matplotlib, Seaborn, and Plotly exercises | Python plus the libraries imported by each script |
| [Semester 5 / CY52](Semester%205/CY52) | First five Advanced Networks lab experiments in Python | Python 3.10+; standard library only |

CYL48's `4.py` expects a `file.csv` in its working directory; that data file is not in this repository. CYL46's `1.sql` starts by dropping and recreating `library_db`, so inspect it before running it against a MySQL instance that already has that database.

## CY52 lab index

| Question | Topic | Folder |
| --- | --- | --- |
| 1 | TCP client/server file transfer | [Question 1](Semester%205/CY52/question_01_tcp_file_transfer) |
| 2 | UDP datagram client/server messages | [Question 2](Semester%205/CY52/question_02_udp_datagrams) |
| 3 | CRC-CCITT generation and verification | [Question 3](Semester%205/CY52/question_03_crc_ccitt) |
| 4 | Client/server checksum generation and verification | [Question 4](Semester%205/CY52/question_04_checksum) |
| 5 | IPv4 fragmentation and reassembly | [Question 5](Semester%205/CY52/question_05_ipv4_fragmentation) |

See the [CY52 course README](Semester%205/CY52/README.md) for the full lab index and test command. Each question folder has its own `README.md` with the task, commands, explanation, and exam points.

## Recent repository changes

- Organized the CY52 lab files into one folder per syllabus question. Related client, server, helper, and sample files now live together.
- Added a README inside each CY52 question folder and a central test suite under `Semester 5/CY52/tests/`.
- Matched professor-corrected student records to the first five CY52 experiments by topic.
- Simplified the CY52 programs to short, interactive lab versions that are easier to learn and reproduce in an exam.
- Expanded every CY52 question README with imports, protocol or algorithm concepts, folder rationale, run instructions, and line-by-line explanations.
- Kept earlier Semester 4 coursework grouped under `Semester 4/CYL46` and `Semester 4/CYL48`.

## Run the CY52 checks

From the repository root:

```bash
cd "Semester 5/CY52"
python3 -m unittest discover -s tests -v
```

The socket examples use `127.0.0.1` by default. Run a server and its client in separate terminals, following the commands in that question's README.
