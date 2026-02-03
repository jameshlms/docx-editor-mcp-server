from collections.abc import Sequence
from textwrap import dedent
from typing import Final, TypedDict

from utils.types import JSONBoolean, JSONNumber, JSONString

EXAMPLE_PAYLOAD: Final[str] = dedent("""\
{
  version: "1",
  configurations: {
    normal_text_style: {
      font_name: "Calibri",
      font_size: 10
    },
    title_text_style: {
      font_name: "Calibri",
      font_size: 16,
      bold: true,
      center: true
    },
    section_header_style: {
      font_name: "Calibri",
      font_size: 11,
      bold: true,
      underline: true
    },
    item_header_style: {
      font_name: "Calibri",
      font_size: 10.5,
      bold: true
    },
    margins: {
      top: 0.5,
      bottom: 0.5,
      left: 0.7,
      right: 0.7
    },
    item_date_style: {
      tab_right: true,
      parentheses_wrap: false,
      date_format: "month_year_short",
      delimiter: " — "
    }
  },

  content: {
    name: "Jane Doe",
    contacts: [
      { type: "location", value: "Austin, TX" },
      { type: "email", value: "jane.doe@example.com"},
      { type: "phone", value: "+1 (555) 555-5555"},
      { type: "linkedin", value: "linkedin.com/in/janedoe"},
      { type: "github", value: "github.com/janedoe"},
      { type: "portfolio", value: "janedoe.dev"}
    ],

    summary: "Data science student focused on data engineering and ML pipelines. Built reproducible ETL workflows, quality checks, and model training/evaluation tooling for analytics and inference.",

    sections: [
      {
        heading: "Experience",
        items: [
          {
            heading: "Data Engineering Intern — Example Company",
            start_date: "2025-05",
            end_date: "2025-08",
            content: "Developed ETL pipelines and data validation checks for analytics and reporting.",
            bullets: [
              "Implemented ingestion jobs with schema checks and monitoring alerts.",
              "Optimized query patterns and reduced pipeline runtime by ~30%.",
              "Partnered with stakeholders to define metrics and data quality SLAs."
            ]
          },
          {
            heading: "Teaching Assistant — Example University",
            start_date: "2024-08",
            end_date: "present",
            content: "Supported undergraduate coursework through labs, grading, and office hours.",
            bullets: [
              "Led weekly lab sessions covering Python fundamentals and data analysis workflows.",
              "Created debugging guides that reduced common assignment errors and regrade requests.",
              "Collaborated with instructors to refine rubrics and improve assignment clarity."
            ]
          }
        ]
      },

      {
        heading: "Projects",
        items: [
          {
            heading: "Credit Card Fraud Detection Pipeline",
            start_date: "2025-09",
            end_date: "2025-12",
            content: "End-to-end pipeline with feature engineering, imbalance handling, evaluation, and export for inference.",
            bullets: [
              "Trained models with PR-focused evaluation and calibrated thresholds for high precision.",
              "Applied sampling and class-weighting strategies for extreme class imbalance; tracked experiments.",
              "Exported the chosen model to ONNX for cross-language serving."
            ]
          },
          {
            heading: "Exoplanet Discovery Method Classification",
            start_date: "2025-01",
            end_date: "2025-04",
            content: "Built a classification model to predict discovery method using NASA exoplanet data.",
            bullets: [
              "Performed reproducible EDA and feature selection with clear documentation.",
              "Trained baseline and tuned models; compared performance across multiple metrics.",
              "Packaged training code for repeatable runs and simple deployment."
            ]
          }
        ]
      },

      {
        heading: "Education",
        items: [
          {
            heading: "B.S. Data Science — Example University",
            start_date: "2023-08",
            end_date: "2027-05",
            content: "Relevant coursework: Data Structures, Database Systems, Machine Learning, Statistics.",
            bullets: null
          }
        ]
      },

      {
        heading: "Skills",
        items: [
          {
            heading: "Programming & Tools",
            start_date: null,
            end_date: null,
            content: "Python, SQL, C#, Git, Docker, Azure, Linux, Pandas, scikit-learn",
            bullets: null
          },
          {
            heading: "Data Engineering",
            start_date: null,
            end_date: null,
            content: "ETL/ELT, dimensional modeling, data validation, orchestration concepts, monitoring/alerting",
            bullets: null
          }
        ]
      }
    ]
  }
}
""").strip()


class TextStyleOptions(TypedDict, total=False):
    font_name: JSONString
    font_size: JSONNumber
    bold: JSONBoolean
    italic: JSONBoolean
    underline: JSONBoolean
    center: JSONBoolean


class MarginOptions(TypedDict, total=False):
    top: JSONNumber
    bottom: JSONNumber
    left: JSONNumber
    right: JSONNumber


class ItemDateStyleOptions(TypedDict, total=False):
    tab_right: JSONBoolean
    parentheses_wrap: JSONBoolean
    date_format: JSONString
    delimiter: JSONString


class ResumeFormatting(TypedDict):
    normal_text_style: TextStyleOptions
    title_text_style: TextStyleOptions
    section_header_style: TextStyleOptions
    item_header_style: TextStyleOptions
    margins: MarginOptions
    item_date_style: ItemDateStyleOptions


class Item(TypedDict, total=False):
    heading: JSONString
    org: JSONString
    location: JSONString
    start_date: JSONString
    end_date: JSONString
    content: JSONString
    bullets: Sequence[JSONString]


class Section(TypedDict):
    heading: JSONString
    items: Sequence[Item]


class Contact(TypedDict, total=False):
    type: JSONString
    display_type: JSONBoolean
    value: JSONString


class ResumeContent(TypedDict, total=False):
    name: JSONString
    contacts: Sequence[JSONString | Contact]
    summary: JSONString
    sections: Sequence[Section]


class Payload(TypedDict):
    version: JSONString
    formatting: ResumeFormatting
    content: ResumeContent
