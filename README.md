# 🎓 Learning Management System (LMS) - Udemy Courses Analysis & Recommendations

This project is a complete Learning Management System (LMS) built using a real-world Udemy course dataset. It integrates **Exploratory Data Analysis (EDA)**, a **Course Recommendation System**, an interactive **Dashboard**, and a **Chatbot** that offers career roadmaps and theoretical knowledge for various skills.

---

## 📌 Project Highlights

- 🔍 **EDA**: Uncovered insights on pricing, course duration, subject popularity, and ratings using visual analysis.
- 🤖 **Recommendation System**: Suggests top Udemy courses based on user's interest or search query.
- 💬 **Chatbot**: Interactively suggests courses, roadmaps for different tech skills, and theory behind the skills.
- 📊 **Dashboard**: Interactive charts and metrics built using Streamlit and Plotly for user-friendly insights.

---

## 📂 Project Structure

```
├── data/                 # Dataset and preprocessed files
    ├── home.py              # Main entry point and navigation
    ├── app.py               # Main application used to run the app
    ├── dashboard.py         # Streamlit dashboard with visual insights
    ├── recommend.py         # Course recommendation logic
    ├── chatbot.py           # Chatbot interface for roadmap and suggestions
├── LMS_EDA.ipynb       # EDA Jupyter Notebook
├── images              # Visuals and screenshots
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```



---

## 📊 Exploratory Data Analysis (EDA)

> 📌 Refer to: [`LMS_EDA.ipynb`](./LMS_EDA.ipynb)

Key insights from Udemy dataset analysis:
- **Web Development** is the most common subject.
- Most courses are priced below ₹5000 with content lengths ranging between 1–3 hours.
- Paid courses have higher enrollments and better ratings.
- Shorter courses tend to be free but have lower ratings and fewer enrollments.

Libraries used: `pandas`, `matplotlib`, `seaborn`, `plotly`

---

## 🤖 Recommendation System

Implemented in [`data/Recommend.py`](./data/Recommend.py):

- Uses **TF-IDF Vectorizer** and **cosine similarity** to suggest relevant courses.
- Inputs: Search keyword (e.g., "Python", "Data Science")
- Outputs: Top 5 matching Udemy courses

---

## 💬 Chatbot for Roadmaps & Theory

Implemented in [`data/chatbot.py`](./data/chatbot.py):

- Acts like a personal learning assistant.
- Accepts natural language queries.
- Provides:
  - Personalized course suggestions
  - Step-by-step roadmap for learning skills (e.g., Web Dev, Python, ML)
  - Brief theory/explanations of each skill domain

---

## 📈 Dashboard

Implemented in [`data/Dashboard.py`](./data/Dashboard.py) using **Streamlit** and **Plotly**.

Dashboard Visualizations:
- 📊 Subject-wise enrollments
- 💰 Price vs. Content Length
- 🎯 Free vs. Paid course analysis
- ⭐ Top-rated courses by subject


## 🚀 How to Run the Project

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/lms-udemy-project.git
cd lms-udemy-project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the main app from the `data/` directory
```bash
streamlit run data/home.py
```

