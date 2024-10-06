# Lossless File Transfer in Local Network

## Index

1. [Overview](#overview)
2. [Features](#features)
3. [How It Works](#how-it-works)
4. [Technologies Used](#technologies-used)
5. [Setup and Usage](#setup-and-usage)
6. [Future Enhancements](#future-enhancements)

## Overview

This project allows for **lossless file transmission** between two systems within the same local network. It ensures that the transferred file is delivered without corruption or data loss by leveraging TCP for reliable transmission and MD5 checksum for validation.

## Features

- **Reliable Data Transfer**: Ensures the ordered and complete delivery of file data using TCP.
- **Checksum Verification**: Uses MD5 hashing to validate that the file was transmitted correctly.
- **Chunked Transmission**: Breaks the file into smaller chunks for efficient, stepwise transfer.
- **Error Detection**: Automatically detects file corruption by comparing checksums.

## How It Works

1. **Sender**:
   - The sender selects a file for transmission.
   - The file’s size and name are sent to the receiver to prepare for receiving.
   - The file is read in chunks and sent sequentially to the receiver.
   - After the full file is transmitted, the sender calculates the MD5 checksum and sends it to the receiver for integrity verification.

2. **Receiver**:
   - The receiver listens for incoming connections from the sender.
   - It receives the file data in chunks and reassembles it locally.
   - After receiving the file, the receiver generates its own MD5 checksum from the received data.
   - The checksum received from the sender is compared with the locally generated one to ensure that the file was not corrupted during transmission.

## Technologies Used

- **Python**
- **Socket Programming** (TCP)
- **MD5 Hashing** (via Python’s `hashlib` module)

## Setup and Usage

To use the system, the **receiver** must be started first, followed by the **sender**. Both systems must be connected to the same network, and their IP addresses and ports should be correctly configured.

### Prerequisites

- Python 3.x installed on both the sender and receiver systems.

### Instructions

1. **Receiver**:
   - Run the receiver system, which waits for a connection from the sender and receives the transmitted file.

2. **Sender**:
   - Run the sender system, specifying the file to be sent and the network details (receiver’s IP and port).

## Future Enhancements

- **Encryption**: Implement file encryption for secure data transmission.
- **Multi-file Transfer**: Add support for sending multiple files in a single session.
- **User Interface**: Develop a graphical interface for ease of use.
