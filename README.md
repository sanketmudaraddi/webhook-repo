Here’s the updated `README.md` for the `webhook-repo`, incorporating the instructions to clone the `action-repo` and perform changes, which will then trigger the webhook:

```markdown
# Webhook Repository

This repository listens for webhook events triggered by actions in the `action-repo`. The events are related to pushes, pull requests, or merges that occur in the `action-repo`. The webhook performs actions like notifying systems, triggering deployment pipelines, or logging event data.

## Table of Contents

- [Overview](#overview)
- [Clone and Setup](#clone-and-setup)
- [How it Works](#how-it-works)
- [Testing the Webhook](#testing-the-webhook)
- [Additional Notes](#additional-notes)
- [UI Changes and MongoDB](#ui-changes-and-mongodb)

## Overview

This repository is responsible for receiving webhook events from the `action-repo` and processing them. When changes occur in the `action-repo`, such as pushes, pull requests, or merges, a webhook is triggered to update the UI, database, or any other necessary actions based on the event.

## Clone and Setup

Follow these steps to clone and set up the webhook repository:

1. **Clone the Webhook Repository**

   First, clone this repository to your local machine:

   ```bash
   git clone https://github.com/sanketmudaraddi/webhook-repo.git
   cd webhook-repo
   ```

2. **Install Python Dependencies**

   This repository uses Python and requires specific dependencies. Install the dependencies listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Webhook Receiver**

   Update the configuration to match your environment. This may include setting the webhook URL, authentication tokens, or logging configurations.

4. **Run the Webhook Server**

   To start the webhook server, run the following command:

   ```bash
   python app.py
   ```

   This will start the server and listen for incoming webhook events.

## How it Works

The webhook repository listens for events sent by the `action-repo`. Here’s a breakdown of the key events that trigger the webhook:

- **Push Event**: When a push occurs in the `action-repo` (e.g., a commit is pushed to the `main` branch), the webhook is triggered. This could update the UI, log the push data, or trigger other actions.
  
- **Pull Request Event**: When a pull request is created or updated in `action-repo`, the webhook is triggered to handle actions like sending notifications or logging pull request details.

- **Merge Event**: When a pull request is merged into the `main` branch (or another branch), the webhook is triggered to perform actions such as deployment, notifications, or logging.

The webhook handler processes the data based on the event type and triggers relevant actions.

## UI Changes and MongoDB

When you push changes to the `action-repo` or open/merge pull requests, the webhook triggers events that affect the UI and MongoDB database. Follow these steps to observe the changes:

1. **Clone the `action-repo`**

   To see the changes reflected in the UI, clone the `action-repo` and make changes to the repository:

   ```bash
   git clone https://github.com/sanketmudaraddi/action-repo.git
   cd action-repo
   ```

2. **Make Changes to `action-repo`**

   You can modify the content in the repository, create new commits, or open/merge pull requests to trigger webhook events. For example, push code to the `main` branch or merge a pull request:

   ```bash
   git checkout -b feature-branch
   # Make changes to files
   git commit -m "Implement new feature"
   git push origin feature-branch
   ```

3. **Push to `action-repo`**

   Once you push your changes to the `action-repo`, the webhook is triggered. It will update the MongoDB database with the event details and reflect the changes in the UI accordingly.

   After the webhook is triggered, you can check the MongoDB database to verify that the events have been stored correctly. Additionally, check the UI to observe the reflected changes.

4. **View UI Changes**

   Once the webhook is triggered by pushing changes to the `action-repo`, visit the UI to view the updates. You will be able to see changes such as:

   - Author details (e.g., who made the change).
   - Timestamps for the events.
   - Branches involved in the event.
   - The action type (push, pull request, merge).

   **Note**: Screenshot for UI changes will be added here.

## Testing the Webhook

To test the webhook functionality:

1. **Trigger an Event in the `action-repo`**:
   - Push changes to the `main` branch or other branches.
   - Open or update a pull request.
   - Merge a pull request.

2. **Check Webhook Logs**:
   - Look for log entries in this repository to confirm that the webhook was triggered and processed correctly.

3. **Verify UI and Database Updates**:
   - Check if the UI has been updated as per the changes in the `action-repo`.
   - Verify that the event data has been correctly logged in MongoDB.

![alt text](<images/Screenshot 2025-01-12 213911.png>)


## Additional Notes

- **Webhook Security**: Ensure that proper security measures are implemented, such as token authentication or IP whitelisting, to allow only trusted sources (like `action-repo`) to trigger the webhook.
  
- **Customization**: You can customize the webhook actions based on your workflow, whether that's triggering deployments, sending notifications, or logging event data.

---


