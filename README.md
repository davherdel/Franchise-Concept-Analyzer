# 🚀 Franchise Concept Analyzer

### Machine Learning-Powered Franchise Potential Evaluation Platform

### `Python` · `XGBoost` · `Streamlit` · `Machine Learning` · `SHAP` · `YouTube Data API v3` · `Predictive Analytics`

> **End-to-end machine learning project combining 74 years of animated television history with IMDb audience signals, Netflix distribution reach, Amazon merchandise indicators, and YouTube engagement data to evaluate the franchise potential of new animated show concepts through an interactive decision-support platform.**

---

## 👤 About This Project

**David Hernandez | Data Analyst**
📍 Lisbon, Portugal · 2026

Franchise Concept Analyzer is the final stage of a broader research initiative exploring what separates successful children's franchises from the thousands of animated shows that never evolve beyond a single series.

Rather than relying on a single dataset, this project combines historical television data, streaming visibility signals, merchandise indicators, audience engagement metrics, and machine learning to identify measurable patterns associated with franchise success.

The result is an interactive Streamlit application capable of evaluating hypothetical animated show concepts and estimating their franchise potential based on historical industry patterns.

---

## 🎯 Business Problem

Launching an animated series requires significant investment, yet evaluating long-term franchise potential remains highly subjective.

Studios, creators, and investors face questions such as:

* Which characteristics are commonly found in successful franchises?
* How important are audience signals compared to creative attributes?
* Do distribution and merchandise opportunities influence franchise outcomes?
* Can historical entertainment data help evaluate new concepts before launch?

This project explores a central question:

> **Can entertainment industry data, audience behavior signals, and machine learning be combined to evaluate the franchise potential of new animated show concepts?**

The objective is not to predict guaranteed success, but to identify patterns consistently associated with stronger franchise outcomes.

---

## 🛠️ Tech Stack

| Tool                    | Usage                                 |
| ----------------------- | ------------------------------------- |
| **Python 3**            | Core analysis and modeling            |
| **Pandas**              | Data cleaning and feature engineering |
| **Scikit-learn**        | Model training and evaluation         |
| **XGBoost**             | Predictive modeling                   |
| **SHAP**                | Explainable AI                        |
| **YouTube Data API v3** | Audience enrichment                   |
| **Streamlit**           | Interactive application               |
| **Matplotlib**          | Model evaluation and reporting        |
| **Jupyter Notebook**    | Research and experimentation workflow |

---

## 🔗 Data Sources & Enrichment Strategy

Rather than relying on a single source, this project combines multiple datasets representing different dimensions of franchise success.

| Source                     | Purpose                                               |
| -------------------------- | ----------------------------------------------------- |
| **IMDb**                   | Ratings, votes, runtime, longevity                    |
| **Netflix**                | Distribution reach and platform visibility            |
| **Amazon Toys**            | Merchandise and commercial potential indicators       |
| **YouTube Data API v3**    | Audience engagement and organic reach                 |
| **Historical TV Metadata** | Genre, country, technique, production characteristics |

The final analytical dataset was built through multiple enrichment stages, transforming fragmented entertainment datasets into a unified franchise evaluation framework.

---

## 📊 Dataset

The final dataset combines:

* Animated TV series spanning approximately **74 years**
* Audience ratings and voting behavior
* Distribution platform indicators
* Merchandise signals
* Production attributes
* Genre classifications
* Country and animation technique information
* Audience reach metrics

Several custom features were engineered to capture relationships between popularity, longevity, audience engagement, and commercial viability.

---

## 🔍 What Was Built

### Section 1 — Data Integration & Feature Engineering

* Combined multiple entertainment datasets
* Standardized franchise-related indicators
* Created predictive features
* Engineered franchise outcome targets
* Built modeling-ready datasets

### Section 2 — Exploratory Analysis

Investigated relationships between:

* Genre and franchise success
* Animation techniques and outcomes
* Runtime and performance
* Country of origin and success rates
* Distribution reach and visibility
* Merchandise indicators and commercial potential

The analysis identified recurring patterns shared by many of the industry's most successful franchises.

### Section 3 — Machine Learning Pipeline

Developed and evaluated multiple predictive models to estimate franchise potential.

Key activities included:

* Feature selection
* Model training and tuning
* Threshold optimization
* Performance evaluation
* Generalization testing

The final solution uses XGBoost as its primary predictive model.

### Section 4 — Explainable AI

SHAP analysis was implemented to:

* Interpret model predictions
* Identify franchise success drivers
* Measure feature influence
* Improve model transparency

This transformed the project from a predictive exercise into a decision-support framework.

### Section 5 — Product Development

Research findings were deployed into an interactive Streamlit application that allows users to:

* Create hypothetical animated show concepts
* Configure production characteristics
* Evaluate franchise potential
* Explore model explanations
* Test alternative concept scenarios

This stage transformed the project from a notebook-based analysis into a usable analytical product.

---

## 🧠 Key Modeling Challenge

One of the most important discoveries emerged during model interpretation.

Initial experiments revealed that YouTube audience reach signals were overwhelmingly dominant predictors of franchise outcomes.

While this improved predictive performance, it created a practical limitation:

> New show concepts have no YouTube audience history.

To improve real-world usability, the final application was redesigned to reduce dependence on post-launch audience metrics and prioritize concept-level characteristics that can be evaluated before production begins.

This project demonstrates not only model development, but also product-oriented machine learning decision-making.

---

## 💡 Key Findings

* Franchise success is influenced by a combination of creative, commercial, and audience-related factors rather than a single dominant characteristic.
* Audience reach signals are highly predictive, but not sufficient on their own.
* Certain genres and production characteristics consistently appear among successful franchises.
* Distribution visibility and merchandise opportunities contribute meaningful predictive value.
* Explainability analysis revealed that only a subset of variables consistently influence model predictions.
* Small concept-level changes can significantly alter estimated franchise potential.

---

## 🤖 Interactive Application

The final deliverable is a Streamlit-powered franchise evaluation platform.

Users can:

* Define a new animated show concept
* Configure production attributes
* Receive a franchise potential estimate
* Explore feature importance insights
* Compare alternative concept designs

The application demonstrates how machine learning can be transformed into a practical decision-support tool.

---

## 📈 Project Deliverables

| Deliverable                      | Description                             |
| -------------------------------- | --------------------------------------- |
| **Jupyter Notebook**             | End-to-end analytical workflow          |
| **Machine Learning Model**       | XGBoost franchise evaluation engine     |
| **SHAP Analysis**                | Explainable AI outputs                  |
| **Visualizations**               | Research and presentation graphics      |
| **Streamlit Application**        | Interactive concept evaluation platform |
| **Feature Engineering Pipeline** | Franchise analysis framework            |

---

## 🚀 Project Highlights

* Built a custom franchise evaluation framework using multiple entertainment datasets
* Integrated IMDb, Netflix, Amazon, and YouTube Data API signals
* Applied explainable AI using SHAP
* Developed an interactive machine learning application
* Transformed historical entertainment research into a practical decision-support platform
* Demonstrated the complete lifecycle from raw data to deployable analytical product
* Access the app here: [Franchise Concept Analyzer](https://franchise-concept-analyzer.streamlit.app/)

---

## About Me

Data Analyst transitioning from 10+ years in IT management and operations, bringing a strong foundation in systems thinking, stakeholder communication, and problem-solving.

I build end-to-end analytical solutions — from data collection and feature engineering to machine learning models, dashboards, and data storytelling — with a focus on transforming data into actionable insights and business value.

📬 [Portfolio](https://davherdel.github.io) · [LinkedIn](https://www.linkedin.com/in/david-hernandez-cr-pt/) · [GitHub](https://github.com/davherdel) · [Tableau Public](https://public.tableau.com/app/profile/david.hernandez6239)
