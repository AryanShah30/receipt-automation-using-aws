# Receipt Automation with AWS

A fully serverless system for automated receipt data extraction and storage, built using AWS. Users can upload image or PDF receipts through a Streamlit interface, triggering a backend pipeline powered by AWS Lambda and Amazon Textract to extract structured fields. Parsed data is stored in DynamoDB, with presigned S3 URLs providing secure file access. Real-time email alerts are sent via SES. The architecture is IAM-secured, scalable, and designed for minimal operational overhead—ideal for automating financial workflows such as expense tracking and invoice management.

---

## Tech Stack

| Layer        | Technology              |
|--------------|--------------------------|
| Frontend     | Streamlit (Python)       |
| Cloud Compute| AWS Lambda               |
| OCR Engine   | Amazon Textract          |
| Storage      | Amazon S3                |
| Database     | Amazon DynamoDB          |
| Notification | Amazon SES               |
| Infra Config | Environment Variables, IAM Roles |

---

## Architecture Overview

This project follows an event-driven, serverless architecture using AWS-native services:

![Architecture Diagram](screenshots/architecture.png)

---

## How It Works

1. **User Upload**: Users upload receipts (images or PDFs) via the Streamlit UI.
2. **Store in S3**: Files are saved to an S3 bucket under the `incoming/` path.
3. **Trigger Lambda**: An S3 event triggers a Lambda function for processing.
4. **Extract with Textract**: Lambda calls Textract to extract structured data like vendor, date, and total amount.
5. **Store in DynamoDB**: The parsed data is cleaned and inserted into a DynamoDB table.
6. **Send Email**: A summary email is sent to a predefined recipient via Amazon SES.
7. **Frontend Display**: Users can view processed receipts in the Streamlit UI, with direct access to files via presigned S3 URLs.

---

## Screenshots

### Streamlit Upload UI
![Upload Screenshot](screenshots/upload.png)

### Processed Receipt Table
![Receipt Table](screenshots/receipts_table.png)

### Email Notification Sample
![Email](screenshots/email.png)

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

For questions or feedback, feel free to connect via [GitHub Issues](https://github.com/AryanShah30/receipt-automation-using-aws/issues).
