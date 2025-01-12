# Webhook Repository

This repository listens for webhook events triggered by actions in the `action-repo`. The webhook is triggered by events like pushes, pull requests, or merges in the `action-repo`, and it performs actions like updating the UI, logging event data, or triggering other systems.

## Clone and Setup

1. **Clone the Webhook Repository**

   Clone this repository to your local machine:

   ```bash
   git clone https://github.com/sanketmudaraddi/webhook-repo.git
   cd webhook-repo
   ```

2. **Install Python Dependencies**

   Install the necessary dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Webhook Server**

   To start the server that listens for incoming webhook events, run:

   ```bash
   python app.py
   ```

## How it Works

The webhook repository listens for events sent from the `action-repo`. These are some key events that will trigger the webhook:

- **Push Event**: When code is pushed to the `action-repo`, the webhook triggers and can perform actions like updating the UI and logging the push details.
- **Pull Request Event**: When a pull request is created or updated, the webhook performs actions such as sending notifications or logging the pull request data.
- **Merge Event**: When a pull request is merged, the webhook performs actions like triggering deployments or updating systems.

## UI Changes and MongoDB

To see how the webhook updates the UI and MongoDB:

1. **Clone the `action-repo`**

   Clone the `action-repo` to make changes that will trigger the webhook:

   ```bash
   git clone https://github.com/sanketmudaraddi/action-repo.git
   cd action-repo
   ```

2. **Make Changes**

   Make changes, create new commits, or open/merge pull requests to trigger events:

   ```bash
   git checkout -b feature-branch
   # Make changes
   git commit -m "Implement new feature"
   git push origin feature-branch
   ```

3. **Check MongoDB and UI**

   After pushing changes to the `action-repo`, check the UI and MongoDB to verify that the webhook has triggered correctly and that the data is logged properly.

   **Note**: ![alt text](<images/Screenshot 2025-01-12 213911.png>)

## Additional Notes

- **Webhook Security**: Ensure security measures like authentication tokens or IP whitelisting are set up to allow only trusted sources (like `action-repo`) to trigger the webhook.
  
- **Customization**: You can adjust the webhook actions according to your needs, whether that's triggering deployments, sending notifications, or logging event data.
```

This version is direct and simple, without the table of contents or additional sections.
