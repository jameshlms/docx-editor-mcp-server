from typing import TypedDict

# {
#   "configurations": {
#     "normal_text_style": {
#       "font_name": "Times New Roman",
#       "font_size": 11.0
#     },
#     "title_text_style": {
#       "font_name": "Times New Roman",
#       "font_size": 18.0,
#       "bold": true
#     },
#     "section_header_style": {
#       "font_name": "Times New Roman",
#       "font_size": 12.0,
#       "bold": true,
#       "underline": true
#     },
#     "item_header_style": {
#       "font_name": "Times New Roman",
#       "font_size": 11.0,
#       "bold": true
#     },
#     "margins": {
#       "top": 0.5,
#       "bottom": 0.5,
#       "left": 0.75,
#       "right": 0.75
#     }
#   },
#   "content": {
#     "name": "James Smith",
#     "contacts": [
#       "Charlotte, NC",
#       { "email": "james.smith@email.com" },
#       { "phone": "+1 (704) 555-0123" },
#       { "linkedin": "linkedin.com/in/jamessmith" },
#       { "github": "github.com/jamessmith" },
#       { "portfolio": "jamessmith.dev" }
#     ],
#     "summary": "Data science student focused on data engineering and ML engineering, building reproducible pipelines and production-ready model serving.",
#     "sections": [
#       {
#         "heading": "Experience",
#         "items": [
#           {
#             "heading": "Teaching Assistant — STAT 1222, UNC Charlotte",
#             "start_date": "Aug 2025",
#             "end_date": "Present",
#             "content": "Supported instruction and grading for introductory statistics; assisted students with problem-solving and tooling.",
#             "bullets": [
#               "Led weekly review sessions and clarified core topics (probability, inference, regression).",
#               "Built lightweight scripts to speed up grading workflows and reduce turnaround time.",
#               "Provided office hours and individualized feedback to improve student performance."
#             ]
#           },
#           {
#             "heading": "Data Engineering Intern — Example Company",
#             "start_date": "May 2025",
#             "end_date": "Aug 2025",
#             "content": "Developed ETL pipelines and data validation checks for analytics and reporting.",
#             "bullets": [
#               "Implemented ingestion jobs with schema checks and monitoring alerts.",
#               "Optimized query patterns and reduced pipeline runtime by ~30%.",
#               "Partnered with stakeholders to define metrics and data quality SLAs."
#             ]
#           }
#         ]
#       },
#       {
#         "heading": "Projects",
#         "items": [
#           {
#             "heading": "Credit Card Fraud Detection Pipeline",
#             "start_date": "Sep 2025",
#             "end_date": "Dec 2025",
#             "content": "End-to-end pipeline with feature engineering, imbalance handling, evaluation, and export for inference.",
#             "bullets": [
#               "Trained models with PR-focused evaluation and calibrated thresholds for high precision.",
#               "Used sampling strategies for extreme class imbalance and tracked experiments.",
#               "Exported the chosen model to ONNX for cross-language serving."
#             ]
#           },
#           {
#             "heading": "Exoplanet Discovery Method Classification",
#             "start_date": "Jan 2025",
#             "end_date": "Apr 2025",
#             "content": "Built a classification model to predict discovery method using NASA exoplanet data.",
#             "bullets": [
#               "Performed reproducible EDA and feature selection with strong documentation.",
#               "Trained baseline and tuned models; compared performance across metrics.",
#               "Packaged training code for repeatable runs and deployment."
#             ]
#           }
#         ]
#       },
#       {
#         "heading": "Education",
#         "items": [
#           {
#             "heading": "B.S. Data Science — University of North Carolina at Charlotte",
#             "start_date": "Aug 2023",
#             "end_date": "May 2027",
#             "content": "Relevant coursework: Data Structures, Database Systems, Machine Learning, Statistics.",
#             "bullets": null
#           }
#         ]
#       },
#       {
#         "heading": "Skills",
#         "items": [
#           {
#             "heading": "Programming & Tools",
#             "start_date": null,
#             "end_date": null,
#             "content": "Python, SQL, C#, Git, Docker, Azure, Linux, Pandas, scikit-learn",
#             "bullets": null
#           }
#         ]
#       }
#     ]
#   }
# }


class TextStyleOptions(TypedDict, total=False):
    font_name: str
    font_size: float
    bold: bool
    italic: bool
    underline: bool
    center: bool


class MarginOptions(TypedDict):
    top: float | None
    bottom: float | None
    left: float | None
    right: float | None


class ItemDateStyleOptions(TypedDict):
    tab_right: bool
    parentheses_wrap: bool
    date_format: str | None
    delimiter: str | None


class ResumeConfigurations(TypedDict):
    normal_text_style: TextStyleOptions
    title_text_style: TextStyleOptions
    section_header_style: TextStyleOptions
    item_header_style: TextStyleOptions
    margins: MarginOptions
    item_date_style: ItemDateStyleOptions


class Item(TypedDict):
    heading: str
    start_date: str | None
    end_date: str | None
    content: str | None
    bullets: list[str] | None


class Section(TypedDict):
    heading: str
    items: list[Item]


class ResumeContent(TypedDict):
    name: str
    contacts: list[str | dict[str, str]]
    summary: str | None
    sections: list[Section]


class Payload(TypedDict):
    configurations: ResumeConfigurations
    content: ResumeContent
