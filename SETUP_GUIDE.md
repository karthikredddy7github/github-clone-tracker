# 🚀 Quick Setup Guide

Follow these steps to get your automated GitHub Clone Tracker running:

## Step 1: Create a Personal Access Token

1. Visit [GitHub Settings → Personal Access Tokens](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Name it: `Clone Tracker`
4. Select scope: ✅ **`repo`** (Full control of private repositories)
5. Click **"Generate token"**
6. **⚠️ IMPORTANT**: Copy the token immediately - you won't see it again!

## Step 2: Create GitHub Repository

1. Create a new repository on GitHub (e.g., `github-clone-tracker`)
2. Make it **Public** or **Private** (your choice)
3. Don't initialize with README (we already have one)

## Step 3: Add Repository Secret

1. Go to your new repository
2. Navigate to **Settings → Secrets and variables → Actions**
3. Click **"New repository secret"**
4. Name: `CLONE_TRACKER_TOKEN`
5. Value: Paste your GitHub personal access token
6. Click **"Add secret"**

## Step 4: Push Code to GitHub

Open your terminal in the `github-clone-tracker` directory and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Make first commit
git commit -m "Initial commit: GitHub Clone Tracker"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/github-clone-tracker.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

## Step 5: Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. If prompted, click **"I understand my workflows, go ahead and enable them"**

## Step 6: Run First Collection (Optional)

Don't want to wait for midnight? Trigger it manually:

1. Go to **Actions** tab
2. Click **"Track Clone Statistics"** workflow
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait 1-2 minutes
5. Check your graphs in the repository!

## ✅ Done!

Your tracker will now run automatically every day at midnight UTC. View your stats anytime by visiting your repository!

---

## 🔍 Verify It's Working

After the first run:
- Check the `clone_data.json` file appears in your repo
- Check the `graphs/` folder has PNG files
- The README should display your graphs

---

## 🛠 Troubleshooting

**Workflow failing?**
- Check your `CLONE_TRACKER_TOKEN` is set correctly
- Ensure your token has the `repo` scope
- Check the Actions logs for specific errors

**No data showing?**
- Clone statistics need a few days of activity to show meaningful data
- Try cloning some of your repositories to generate test data

---

**Need help?** Check the [main README](README.md) for more details!
