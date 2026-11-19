"""
Aurelia Grand — Trilingual Luxury Hotel CRM & AI Guest Concierge
Production-ready, single-file Streamlit application optimized for GitHub & Streamlit Community Cloud.
Supports 100% isolated English (LTR), Persian (RTL), and Arabic (RTL) localization.
"""

from __future__ import annotations

import datetime
import html
import io
import json
import os
import random
import string
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
from google import genai
from google.genai import types

# =============================================================================
# 1. GLOBAL CONSTANTS & STORAGE PATHS
# =============================================================================

GEMINI_MODEL = "gemini-2.5-flash"

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "hotel_config.json"
BOOKINGS_FILE = BASE_DIR / "bookings.json"

DEFAULT_HERO_IMAGE = (
    "https://images.unsplash.com/photo-1582719508461-905c673771fd"
    "?auto=format&fit=crop&w=1600&q=85"
)

ROOM_KEYS = ["single", "double", "twin", "junior_suite", "royal_suite"]
GUEST_KEYS = ["1_adult", "2_adults", "2_adults_1_child", "family_group"]
SERVICE_KEYS = [
    "airport_vip",
    "breakfast",
    "late_checkout",
    "spa_massage",
    "honeymoon_decor",
]
AMENITY_KEYS = [
    "wifi",
    "spa_pool",
    "airport_transfer",
    "rooftop_dining",
    "room_service",
    "city_tour",
    "fitness_center",
    "valet_parking",
]
STATUS_KEYS = ["Pending", "Confirmed", "Completed", "Cancelled"]

LANGUAGE_OPTIONS = {
    "en": "English",
    "fa": "فارسی",
    "ar": "العربية",
}

DEFAULT_HOTEL_CONFIG: dict[str, Any] = {
    "name": {
        "en": "Aurelia Grand Palace Hotel",
        "fa": "هتل مجلل آئورلیا گرند پالاس",
        "ar": "فندق قصر أوريليا جراند الفاخر",
    },
    "tagline": {
        "en": "Timeless Coastal Elegance & Bespoke Five-Star Hospitality",
        "fa": "شکوه ماندگار ساحلی و میزبانی پنج‌ستاره اختصاصی",
        "ar": "أناقة ساحلية خالدة وضيافة فاخرة من فئة خمس نجوم",
    },
    "description": {
        "en": (
            "Overlooking serene azure waters, Aurelia Grand Palace Hotel blends architectural "
            "grandeur with intimate, personalized service. Guests enjoy sunlit limestone suites, "
            "a candlelit thermal spa sanctuary, panoramic rooftop gastronomy, and effortless "
            "access to cultural landmarks and private coastal promenades."
        ),
        "fa": (
            "هتل مجلل آئورلیا گرند پالاس با چشم‌اندازی خیره‌کننده به آب‌های نیلگون، شکوه معماری "
            "اصیل را با خدمات اختصاصی و گرم در هم می‌آمیزد. مهمانان در سوئیت‌های آفتاب‌گیر، "
            "مجموعه اسپا و استخر حرارتی، رستوران پانورامای بام و دسترسی آسان به جاذبه‌های "
            "فرهنگی و ساحلی تجربه‌ای فراموش‌نشدنی خواهند داشت."
        ),
        "ar": (
            "يطل فندق قصر أوريليا جراند على المياه الزرقاء الهادئة، حيث يمزج بين الفخامة المعمارية "
            "والخدمة الشخصية الراقية. يستمتع الضيوف بأجنحة فسيحة، ومنتجع سبا حراري هادئ، "
            "ومطعم بانورامي على السطح مع وصول سلس إلى المعالم الثقافية والكورنيش الساحلي."
        ),
    },
    "address": {
        "en": "188 Corniche Marina Boulevard, Pearl Bay District",
        "fa": "بلوار ساحلی مارینا، پلاک ۱۸۸، منطقه خلیج مروارید",
        "ar": "شارع كورنيش المارينا ١٨٨، حي خليج اللؤلؤ",
    },
    "star_rating": 5,
    "phone": "+971 4 555 0198",
    "email": "concierge@aureliagrand.com",
    "check_in_time": "15:00",
    "check_out_time": "12:00",
    "hero_image_url": DEFAULT_HERO_IMAGE,
    "latitude": 25.2048,
    "longitude": 55.2708,
    "currency": "USD",
    "room_prices": {
        "single": 180,
        "double": 260,
        "twin": 250,
        "junior_suite": 420,
        "royal_suite": 780,
    },
    "service_prices": {
        "airport_vip": 95,
        "breakfast": 35,
        "late_checkout": 60,
        "spa_massage": 140,
        "honeymoon_decor": 120,
    },
    "active_amenities": [
        "wifi",
        "spa_pool",
        "airport_transfer",
        "rooftop_dining",
        "room_service",
        "city_tour",
        "fitness_center",
        "valet_parking",
    ],
    "gemini_model": GEMINI_MODEL,
    "admin_pin": "1234",
}

# =============================================================================
# 2. 100% ISOLATED TRILINGUAL TRANSLATIONS DICTIONARY
# =============================================================================

TRANSLATIONS: dict[str, dict[str, Any]] = {
    "en": {
        "dir": "ltr",
        "align": "left",
        "font_family": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
        "font_import": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
        "language_name_for_ai": "English",
        "sidebar_lang_label": "Interface Language",
        "sidebar_hotel_info": "Direct Concierge Desk",
        "sidebar_phone": "Phone",
        "sidebar_email": "Email",
        "sidebar_checkin": "Check-in",
        "sidebar_checkout": "Check-out",
        "sidebar_ai_section": "AI Concierge Configuration",
        "sidebar_api_key_label": "Gemini API Key (Optional Override)",
        "sidebar_api_key_help": "Reads GEMINI_API_KEY from Streamlit Secrets or environment automatically. Paste a key here to test immediately.",
        "sidebar_api_ready": "Gemini API Key: Connected",
        "sidebar_api_missing": "Gemini API Key: Not Configured",
        "sidebar_model_label": "Active AI Model",
        "star_badge": "{stars}-Star Luxury Hospitality",
        "hero_checkin_label": "Check-in",
        "hero_checkout_label": "Check-out",
        "tabs": [
            "Overview & Location",
            "Book a Stay & Services",
            "AI Receptionist",
            "Hotel Management",
        ],
        # Tab 1
        "overview_about_title": "About the Property",
        "overview_details_title": "Essential Stay Information",
        "overview_address_label": "Address",
        "overview_phone_label": "Reservations & Desk",
        "overview_email_label": "Guest Relations Email",
        "overview_hours_label": "Check-in / Check-out",
        "overview_amenities_title": "Hotel Amenities & Guest Attractions",
        "overview_amenities_empty": "No active amenities configured yet.",
        "overview_map_title": "Geographic Location & Directions",
        "overview_map_caption": "Interactive property coordinates: Latitude {lat:.4f}, Longitude {lon:.4f}",
        "amenity_categories": {
            "connectivity": "Connectivity & Comfort",
            "wellness": "Wellness & Dining",
            "concierge": "Transfers & Experiences",
        },
        "amenities": {
            "wifi": ("Free High-Speed Wi-Fi", "Fiber-optic connectivity across all suites and lounges", "connectivity"),
            "spa_pool": ("Spa & Infinity Pool", "Thermal plunge pool, sauna, and signature massages", "wellness"),
            "airport_transfer": ("VIP Airport Transfer", "Private chauffeured luxury sedan upon arrival", "concierge"),
            "rooftop_dining": ("Rooftop Restaurant", "Panoramic coastal terrace with seasonal fine dining", "wellness"),
            "room_service": ("24/7 In-Room Dining", "Curated culinary service delivered around the clock", "connectivity"),
            "city_tour": ("City Tour & Cultural Desk", "Tailored local excursions and private guides", "concierge"),
            "fitness_center": ("Panoramic Fitness Studio", "Modern cardio and strength suite open 24 hours", "wellness"),
            "valet_parking": ("Complimentary Valet Parking", "Secure underground parking with EV charging", "concierge"),
        },
        # Tab 2
        "booking_title": "Smart Room Reservation & Guest Services",
        "booking_subtitle": "Select your room configuration, travel dates, and bespoke services to view an instant stay estimate.",
        "booking_step_stay": "1. Stay Dates, Room & Bespoke Services",
        "booking_step_guest": "2. Guest Contact Details & Confirmation",
        "checkin_date": "Check-in Date",
        "checkout_date": "Check-out Date",
        "room_type": "Room Type & Bed Configuration",
        "num_guests": "Number of Guests",
        "extra_services": "Extra Guest Services",
        "guest_name": "Guest Full Name *",
        "guest_name_ph": "e.g. Elena Rostova",
        "guest_phone": "Phone / WhatsApp Number *",
        "guest_phone_ph": "e.g. +971 50 123 4567",
        "guest_email": "Email Address *",
        "guest_email_ph": "e.g. guest@example.com",
        "special_notes": "Special Requests & Arrival Notes",
        "special_notes_ph": "Dietary preferences, pillow choice, flight number, or special celebrations...",
        "submit_booking_btn": "Confirm Reservation Request",
        "rooms": {
            "single": "Single Room (1 Single Bed)",
            "double": "Double Room (1 King Bed)",
            "twin": "Twin Room (2 Single Beds)",
            "junior_suite": "Junior Suite (King Bed + Lounge)",
            "royal_suite": "Royal Family Suite (2 Bedrooms)",
        },
        "guests": {
            "1_adult": "1 Adult",
            "2_adults": "2 Adults",
            "2_adults_1_child": "2 Adults + 1 Child",
            "family_group": "Family / Group (4+)",
        },
        "services": {
            "airport_vip": "Airport VIP Pickup",
            "breakfast": "Breakfast Included (Per Night)",
            "late_checkout": "Late Check-out (Until 16:00)",
            "spa_massage": "Spa & Massage Package",
            "honeymoon_decor": "Honeymoon Room Decoration",
        },
        "estimate_title": "Live Stay Summary & Estimated Total",
        "estimate_nights": "Duration",
        "estimate_nights_val": "{n} Night(s)",
        "estimate_room_rate": "Nightly Room Rate",
        "estimate_room_subtotal": "Accommodation Subtotal",
        "estimate_services_subtotal": "Selected Extra Services",
        "estimate_total": "Estimated Total",
        "estimate_per_night": "/ night",
        "estimate_invalid_dates": "Check-out date must be at least 1 day after Check-in date.",
        "val_missing_fields": "Please complete Guest Full Name, Phone/WhatsApp, and Email Address before submitting.",
        "val_invalid_email": "Please enter a valid email address.",
        "val_invalid_dates": "Check-out date must be later than Check-in date.",
        "booking_confirmed_title": "Reservation Request Confirmed",
        "booking_confirmed_desc": "Thank you, {name}. Our reservations concierge has received your inquiry and will reach out shortly.",
        "booking_ref_label": "Booking Reference Code",
        "booking_summary_line": "{room} · {nights} Night(s) · Estimated Total: {currency} {total:,.0f}",
        # Tab 3
        "ai_title": "AI Hotel Concierge & Receptionist",
        "ai_subtitle": "Ask about suites, nightly rates, amenities, check-in policies, or personalized stay recommendations.",
        "ai_welcome": "Welcome to {hotel}. I am your dedicated AI Concierge. How may I assist you with your stay today?",
        "ai_quick_prompts_label": "Suggested Questions",
        "ai_quick_prompts": [
            "What room types and nightly rates do you offer?",
            "Tell me about hotel amenities and check-in/check-out times.",
            "Help me choose the best suite for a family stay with spa services.",
        ],
        "ai_input_placeholder": "Ask our AI Receptionist anything about your stay...",
        "ai_clear_chat": "Clear Conversation",
        "ai_thinking": "Consulting hotel concierge desk...",
        "ai_missing_key_error": "Gemini API key is not configured yet. Please add GEMINI_API_KEY in Streamlit Secrets or enter a temporary key in the sidebar.",
        "ai_api_error": "The AI Concierge encountered a temporary connection issue. Please verify your API key or model name in Hotel Management and try again.",
        "ai_system_instruction": (
            "You are the warm, refined, five-star AI Hotel Concierge and Receptionist for {hotel_name}. "
            "CRITICAL LANGUAGE RULE: You MUST reply EXCLUSIVELY in English. Never mix words from Persian or Arabic. "
            "Use ONLY the verified live hotel facts below. If asked something outside these facts, politely offer to connect "
            "the guest with the front desk at {phone} or {email}. Keep responses clear, gracious, and concise.\n\n"
            "LIVE HOTEL PROFILE:\n{profile}"
        ),
        # Tab 4
        "admin_title": "Hotel Owner Admin & White-Label Customizer",
        "admin_pin_prompt": "Enter Management PIN to unlock White-Label Settings & CRM Dashboard",
        "admin_pin_demo_note": "Demo Access PIN: 1234",
        "admin_pin_label": "Management PIN",
        "admin_unlock_btn": "Unlock Management Panel",
        "admin_lock_btn": "Lock Panel",
        "admin_wrong_pin": "Incorrect PIN. Please try again (default demo PIN is 1234).",
        "admin_section_a": "Section A — White-Label Hotel Customizer",
        "admin_section_b": "Section B — Bookings & CRM Dashboard",
        "admin_customizer_expand": "Expand to Customize Hotel Brand, Rates, Amenities & AI Model",
        "cfg_names_group": "Hotel Branding (English, Persian, Arabic)",
        "cfg_name_en": "Hotel Name (English)",
        "cfg_name_fa": "Hotel Name (Persian)",
        "cfg_name_ar": "Hotel Name (Arabic)",
        "cfg_tagline_en": "Tagline (English)",
        "cfg_tagline_fa": "Tagline (Persian)",
        "cfg_tagline_ar": "Tagline (Arabic)",
        "cfg_desc_en": "Description (English)",
        "cfg_desc_fa": "Description (Persian)",
        "cfg_desc_ar": "Description (Arabic)",
        "cfg_addr_en": "Address (English)",
        "cfg_addr_fa": "Address (Persian)",
        "cfg_addr_ar": "Address (Arabic)",
        "cfg_contact_group": "Property Details, Media & Map Coordinates",
        "cfg_stars": "Star Rating",
        "cfg_phone": "Phone Number",
        "cfg_email": "Contact Email",
        "cfg_checkin": "Check-in Time",
        "cfg_checkout": "Check-out Time",
        "cfg_currency": "Currency Code",
        "cfg_hero_url": "Hero Banner Image URL",
        "cfg_lat": "Latitude",
        "cfg_lon": "Longitude",
        "cfg_pricing_group": "Nightly Room Base Prices & Amenities",
        "cfg_amenities_label": "Active Hotel Amenities",
        "cfg_ai_group": "AI Concierge & Security Settings",
        "cfg_gemini_model": "Gemini Model Name",
        "cfg_admin_pin": "Management PIN",
        "cfg_save_btn": "Save Hotel Settings",
        "cfg_saved_msg": "Hotel settings saved to hotel_config.json and applied immediately.",
        "kpi_total": "Total Inquiries",
        "kpi_pending": "Pending Requests",
        "kpi_confirmed": "Confirmed Bookings",
        "kpi_revenue": "Estimated Revenue",
        "crm_no_bookings": "No guest reservations have been submitted yet. New bookings from Tab 2 will appear here automatically.",
        "crm_update_title": "Update Reservation Status",
        "crm_select_booking": "Select Booking Reference",
        "crm_select_status": "New Status",
        "crm_update_btn": "Save Status Update",
        "crm_status_updated": "Booking {ref} updated to {status}.",
        "crm_download_csv": "Download Bookings (CSV)",
        "statuses": {
            "Pending": "Pending",
            "Confirmed": "Confirmed",
            "Completed": "Completed",
            "Cancelled": "Cancelled",
        },
        "table_cols": {
            "ref_id": "Reference ID",
            "created_at": "Submitted",
            "guest_name": "Guest Name",
            "phone": "Phone / WhatsApp",
            "email": "Email",
            "check_in": "Check-in",
            "check_out": "Check-out",
            "nights": "Nights",
            "room_type": "Room Type",
            "guests": "Guests",
            "services": "Extra Services",
            "estimated_total": "Estimated Total",
            "status": "Status",
            "notes": "Special Notes",
        },
    },
    "fa": {
        "dir": "rtl",
        "align": "right",
        "font_family": "'Vazirmatn', Tahoma, sans-serif",
        "font_import": "https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700&display=swap",
        "language_name_for_ai": "Persian (فارسی)",
        "sidebar_lang_label": "زبان سامانه",
        "sidebar_hotel_info": "میز پذیرش و ارتباط مستقیم",
        "sidebar_phone": "تلفن تماس",
        "sidebar_email": "ایمیل",
        "sidebar_checkin": "ساعت تحویل اتاق",
        "sidebar_checkout": "ساعت تخلیه اتاق",
        "sidebar_ai_section": "تنظیمات دستیار هوشمند",
        "sidebar_api_key_label": "کلید Gemini API (اختیاری)",
        "sidebar_api_key_help": "کلید GEMINI_API_KEY به‌صورت خودکار از Secrets یا متغیر محیطی خوانده می‌شود. برای تست فوری می‌توانید کلید خود را اینجا وارد کنید.",
        "sidebar_api_ready": "وضعیت کلید Gemini: متصل",
        "sidebar_api_missing": "وضعیت کلید Gemini: تنظیم نشده",
        "sidebar_model_label": "مدل هوش مصنوعی فعال",
        "star_badge": "اقامتگاه لوکس {stars} ستاره",
        "hero_checkin_label": "تحویل اتاق",
        "hero_checkout_label": "تخلیه اتاق",
        "tabs": [
            "مرور کلی و موقعیت مکانی",
            "رزرو اتاق و خدمات",
            "دستیار هوشمند پذیرش",
            "مدیریت هتل",
        ],
        # Tab 1
        "overview_about_title": "درباره هتل",
        "overview_details_title": "اطلاعات ضروری اقامت",
        "overview_address_label": "نشانی هتل",
        "overview_phone_label": "رزرواسیون و پذیرش",
        "overview_email_label": "ایمیل امور مهمانان",
        "overview_hours_label": "ساعات تحویل و تخلیه",
        "overview_amenities_title": "امکانات رفاهی و جاذبه‌های مهمانان",
        "overview_amenities_empty": "هنوز امکاناتی فعال نشده است.",
        "overview_map_title": "موقعیت جغرافیایی و نقشه دسترسی",
        "overview_map_caption": "مختصات دقیق هتل: عرض جغرافیایی {lat:.4f}، طول جغرافیایی {lon:.4f}",
        "amenity_categories": {
            "connectivity": "آسایش و ارتباطات",
            "wellness": "تندرستی و پذیرایی",
            "concierge": "ترانسفر و تجربه‌های شهری",
        },
        "amenities": {
            "wifi": ("اینترنت پرسرعت رایگان", "اتصال فیبر نوری در تمامی سوئیت‌ها و لابی", "connectivity"),
            "spa_pool": ("اسپا و استخر بی‌نهایت", "استخر حرارتی، سونا و خدمات تخصصی ماساژ", "wellness"),
            "airport_transfer": ("ترانسفر فرودگاهی ویژه", "خودروی لوکس با راننده اختصاصی در بدو ورود", "concierge"),
            "rooftop_dining": ("رستوران پانورامای بام", "تراس ساحلی با منوی فصلی سرآشپز", "wellness"),
            "room_service": ("سرویس اتاق ۲۴ ساعته", "پذیرایی اختصاصی در اتاق در تمام ساعات شبانه‌روز", "connectivity"),
            "city_tour": ("میز گردشگری و تور شهری", "برنامه‌ریزی گشت‌های فرهنگی با راهنمای اختصاصی", "concierge"),
            "fitness_center": ("باشگاه بدنسازی پانوراما", "سالن ورزشی مدرن با دسترسی ۲۴ ساعته", "wellness"),
            "valet_parking": ("پارکینگ اختصاصی با والت", "پارکینگ مسقف ایمن همراه با شارژر خودرو برقی", "concierge"),
        },
        # Tab 2
        "booking_title": "رزرو هوشمند اتاق و خدمات مهمان",
        "booking_subtitle": "نوع اتاق، تاریخ اقامت و خدمات دلخواه را انتخاب کنید تا برآورد هزینه به‌صورت لحظه‌ای نمایش داده شود.",
        "booking_step_stay": "۱. تاریخ اقامت، نوع اتاق و خدمات اضافی",
        "booking_step_guest": "۲. مشخصات مهمان و ثبت درخواست رزرو",
        "checkin_date": "تاریخ ورود",
        "checkout_date": "تاریخ خروج",
        "room_type": "نوع اتاق و چیدمان تخت",
        "num_guests": "تعداد مهمانان",
        "extra_services": "خدمات ویژه و اضافی",
        "guest_name": "نام و نام خانوادگی مهمان *",
        "guest_name_ph": "مثلاً: سارا محمدی",
        "guest_phone": "شماره تماس / واتساپ *",
        "guest_phone_ph": "مثلاً: 09123456789",
        "guest_email": "نشانی ایمیل *",
        "guest_email_ph": "مثلاً: guest@example.com",
        "special_notes": "توضیحات و درخواست‌های ویژه",
        "special_notes_ph": "رژیم غذایی، ساعت پرواز، درخواست تخت کودک یا تزیینات مناسبتی...",
        "submit_booking_btn": "ثبت نهایی درخواست رزرو",
        "rooms": {
            "single": "اتاق یک‌نفره (۱ تخت سینگل)",
            "double": "اتاق دونفره دبل (۱ تخت کینگ)",
            "twin": "اتاق دونفره توئین (۲ تخت سینگل)",
            "junior_suite": "جونیور سوئیت (تخت کینگ + نشیمن)",
            "royal_suite": "سوئیت رویال خانوادگی (۲ خوابه)",
        },
        "guests": {
            "1_adult": "۱ بزرگسال",
            "2_adults": "۲ بزرگسال",
            "2_adults_1_child": "۲ بزرگسال + ۱ کودک",
            "family_group": "خانواده / گروهی (۴ نفر به بالا)",
        },
        "services": {
            "airport_vip": "ترانسفر فرودگاهی VIP",
            "breakfast": "صبحانه کامل (به‌ازای هر شب)",
            "late_checkout": "تخلیه دیرهنگام (تا ساعت ۱۶:۰۰)",
            "spa_massage": "پکیج اسپا و ماساژ",
            "honeymoon_decor": "تزیین اتاق ماه‌عسل",
        },
        "estimate_title": "پیش‌نمایش خلاصه اقامت و برآورد هزینه",
        "estimate_nights": "مدت اقامت",
        "estimate_nights_val": "{n} شب",
        "estimate_room_rate": "نرخ هر شب اتاق",
        "estimate_room_subtotal": "جمع هزینه اقامت",
        "estimate_services_subtotal": "جمع خدمات اضافی انتخاب‌شده",
        "estimate_total": "برآورد مبلغ کل",
        "estimate_per_night": "/ هر شب",
        "estimate_invalid_dates": "تاریخ خروج باید حداقل یک روز پس از تاریخ ورود باشد.",
        "val_missing_fields": "لطفاً نام و نام خانوادگی، شماره تماس و نشانی ایمیل را تکمیل کنید.",
        "val_invalid_email": "لطفاً یک نشانی ایمیل معتبر وارد کنید.",
        "val_invalid_dates": "تاریخ خروج باید بعد از تاریخ ورود باشد.",
        "booking_confirmed_title": "درخواست رزرو با موفقیت ثبت شد",
        "booking_confirmed_desc": "سپاسگزاریم {name} عزیز. درخواست شما در واحد رزرواسیون ثبت شد و کارشناسان ما به‌زودی با شما تماس می‌گیرند.",
        "booking_ref_label": "کد پیگیری رزرو",
        "booking_summary_line": "{room} · {nights} شب · برآورد کل: {currency} {total:,.0f}",
        # Tab 3
        "ai_title": "دستیار هوشمند پذیرش و راهنمای مهمان",
        "ai_subtitle": "درباره اتاق‌ها، تعرفه‌ها، امکانات هتل، قوانین پذیرش یا انتخاب سوئیت مناسب بپرسید.",
        "ai_welcome": "به {hotel} خوش آمدید. من دستیار هوشمند پذیرش شما هستم. چطور می‌توانم در برنامه‌ریزی اقامتتان کمکتان کنم؟",
        "ai_quick_prompts_label": "پرسش‌های پیشنهادی",
        "ai_quick_prompts": [
            "چه نوع اتاق‌هایی دارید و قیمت هر شب چقدر است؟",
            "درباره امکانات هتل و ساعت تحویل و تخلیه اتاق توضیح دهید.",
            "برای یک اقامت خانوادگی همراه با خدمات اسپا کدام سوئیت مناسب‌تر است؟",
        ],
        "ai_input_placeholder": "سؤال خود را از دستیار هوشمند هتل بپرسید...",
        "ai_clear_chat": "پاک‌سازی گفتگو",
        "ai_thinking": "در حال دریافت پاسخ از میز پذیرش هوشمند...",
        "ai_missing_key_error": "کلید Gemini API تنظیم نشده است. لطفاً GEMINI_API_KEY را در تنظیمات Secrets ثبت کنید یا در نوار کناری وارد نمایید.",
        "ai_api_error": "در اتصال به دستیار هوشمند خطای موقتی رخ داد. لطفاً کلید API یا نام مدل را در بخش مدیریت هتل بررسی کنید.",
        "ai_system_instruction": (
            "شما دستیار هوشمند پذیرش و کانسییرژ پنج‌ستاره و بسیار مودب هتل {hotel_name} هستید. "
            "قانون حیاتی زبان: شما باید منحصراً و ۱۰۰٪ به زبان فارسی پاسخ دهید و هیچ کلمه انگلیسی یا عربی غیرضروری به کار نبرید. "
            "فقط بر اساس اطلاعات واقعی و زنده زیر پاسخ دهید. اگر سوالی خارج از این اطلاعات بود، با احترام مهمان را به تماس با پذیرش "
            "({phone} یا {email}) راهنمایی کنید. پاسخ‌ها گرم، حرفه‌ای و دقیق باشند.\n\n"
            "اطلاعات زنده هتل:\n{profile}"
        ),
        # Tab 4
        "admin_title": "پنل مدیریت هتل و سفارشی‌سازی برند",
        "admin_pin_prompt": "برای دسترسی به تنظیمات برند و داشبورد رزرواسیون، کد پین مدیریت را وارد کنید",
        "admin_pin_demo_note": "کد پین پیش‌فرض دمو: 1234",
        "admin_pin_label": "کد پین مدیریت",
        "admin_unlock_btn": "ورود به پنل مدیریت",
        "admin_lock_btn": "قفل کردن پنل",
        "admin_wrong_pin": "کد پین نادرست است. لطفاً مجدداً تلاش کنید (پین پیش‌فرض دمو: 1234).",
        "admin_section_a": "بخش اول — سفارشی‌سازی برند و اطلاعات هتل",
        "admin_section_b": "بخش دوم — داشبورد رزرواسیون و مدیریت مشتریان (CRM)",
        "admin_customizer_expand": "باز کردن تنظیمات برند، نرخ اتاق‌ها، امکانات و مدل هوش مصنوعی",
        "cfg_names_group": "هویت برند هتل (انگلیسی، فارسی، عربی)",
        "cfg_name_en": "نام هتل (انگلیسی)",
        "cfg_name_fa": "نام هتل (فارسی)",
        "cfg_name_ar": "نام هتل (عربی)",
        "cfg_tagline_en": "شعار تبلیغاتی (انگلیسی)",
        "cfg_tagline_fa": "شعار تبلیغاتی (فارسی)",
        "cfg_tagline_ar": "شعار تبلیغاتی (عربی)",
        "cfg_desc_en": "توضیحات هتل (انگلیسی)",
        "cfg_desc_fa": "توضیحات هتل (فارسی)",
        "cfg_desc_ar": "توضیحات هتل (عربی)",
        "cfg_addr_en": "نشانی (انگلیسی)",
        "cfg_addr_fa": "نشانی (فارسی)",
        "cfg_addr_ar": "نشانی (عربی)",
        "cfg_contact_group": "اطلاعات تماس، تصویر بنر و مختصات نقشه",
        "cfg_stars": "درجه ستاره هتل",
        "cfg_phone": "شماره تلفن",
        "cfg_email": "ایمیل تماس",
        "cfg_checkin": "ساعت تحویل اتاق",
        "cfg_checkout": "ساعت تخلیه اتاق",
        "cfg_currency": "واحد پول",
        "cfg_hero_url": "نشانی تصویر بنر اصلی",
        "cfg_lat": "عرض جغرافیایی",
        "cfg_lon": "طول جغرافیایی",
        "cfg_pricing_group": "قیمت پایه هر شب اتاق‌ها و امکانات فعال",
        "cfg_amenities_label": "امکانات فعال هتل",
        "cfg_ai_group": "تنظیمات هوش مصنوعی و امنیت",
        "cfg_gemini_model": "نام مدل Gemini",
        "cfg_admin_pin": "کد پین مدیریت",
        "cfg_save_btn": "ذخیره تنظیمات هتل",
        "cfg_saved_msg": "تنظیمات هتل با موفقیت در فایل hotel_config.json ذخیره و اعمال شد.",
        "kpi_total": "کل درخواست‌ها",
        "kpi_pending": "در انتظار بررسی",
        "kpi_confirmed": "رزروهای تأییدشده",
        "kpi_revenue": "درآمد برآوردی",
        "crm_no_bookings": "هنوز هیچ درخواست رزروی ثبت نشده است. رزروهای جدید از تب دوم بلافاصله اینجا نمایش داده می‌شوند.",
        "crm_update_title": "به‌روزرسانی وضعیت رزرو",
        "crm_select_booking": "انتخاب کد پیگیری رزرو",
        "crm_select_status": "وضعیت جدید",
        "crm_update_btn": "ثبت تغییر وضعیت",
        "crm_status_updated": "وضعیت رزرو {ref} به «{status}» تغییر یافت.",
        "crm_download_csv": "دانلود گزارش رزروها (CSV)",
        "statuses": {
            "Pending": "در انتظار بررسی",
            "Confirmed": "تأییدشده",
            "Completed": "تکمیل‌شده",
            "Cancelled": "لغوشده",
        },
        "table_cols": {
            "ref_id": "کد پیگیری",
            "created_at": "زمان ثبت",
            "guest_name": "نام مهمان",
            "phone": "تلفن / واتساپ",
            "email": "ایمیل",
            "check_in": "تاریخ ورود",
            "check_out": "تاریخ خروج",
            "nights": "شب‌ها",
            "room_type": "نوع اتاق",
            "guests": "تعداد مهمان",
            "services": "خدمات اضافی",
            "estimated_total": "برآورد هزینه",
            "status": "وضعیت",
            "notes": "توضیحات",
        },
    },
    "ar": {
        "dir": "rtl",
        "align": "right",
        "font_family": "'Cairo', Tahoma, sans-serif",
        "font_import": "https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700&display=swap",
        "language_name_for_ai": "Arabic (العربية)",
        "sidebar_lang_label": "لغة النظام",
        "sidebar_hotel_info": "مكتب الاستقبال المباشر",
        "sidebar_phone": "الهاتف",
        "sidebar_email": "البريد الإلكتروني",
        "sidebar_checkin": "تسجيل الوصول",
        "sidebar_checkout": "تسجيل المغادرة",
        "sidebar_ai_section": "إعدادات المساعد الذكي",
        "sidebar_api_key_label": "مفتاح Gemini API (اختياري)",
        "sidebar_api_key_help": "يقرأ النظام GEMINI_API_KEY تلقائياً من الأسرار أو البيئة. يمكنك إدخال مفتاح هنا للتجربة الفورية.",
        "sidebar_api_ready": "مفتاح Gemini: متصل",
        "sidebar_api_missing": "مفتاح Gemini: غير مضبوط",
        "sidebar_model_label": "نموذج الذكاء الاصطناعي",
        "star_badge": "ضيافة فاخرة {stars} نجوم",
        "hero_checkin_label": "الوصول",
        "hero_checkout_label": "المغادرة",
        "tabs": [
            "نظرة عامة والموقع",
            "حجز الإقامة والخدمات",
            "مساعد الاستقبال الذكي",
            "إدارة الفندق",
        ],
        # Tab 1
        "overview_about_title": "نبذة عن الفندق",
        "overview_details_title": "معلومات الإقامة الأساسية",
        "overview_address_label": "العنوان",
        "overview_phone_label": "الحجوزات والاستقبال",
        "overview_email_label": "بريد علاقات الضيوف",
        "overview_hours_label": "مواعيد الوصول والمغادرة",
        "overview_amenities_title": "مرافق الفندق ومعالم الضيوف",
        "overview_amenities_empty": "لا توجد مرافق مفعلة حالياً.",
        "overview_map_title": "الموقع الجغرافي والخريطة التفاعلية",
        "overview_map_caption": "إحداثيات الفندق: خط العرض {lat:.4f}، خط الطول {lon:.4f}",
        "amenity_categories": {
            "connectivity": "الراحة والاتصال",
            "wellness": "العافية والمطاعم",
            "concierge": "التنقلات والتجارب",
        },
        "amenities": {
            "wifi": ("إنترنت فائق السرعة مجاني", "اتصال ألياف ضوئية في جميع الأجنحة والردهات", "connectivity"),
            "spa_pool": ("السبا والمسبح اللامتناهي", "مسبح حراري وساونا وجلسات مساج فاخرة", "wellness"),
            "airport_transfer": ("توصيل المطار لكبار الشخصيات", "سيارة فاخرة مع سائق خاص عند الوصول", "concierge"),
            "rooftop_dining": ("مطعم السطح البانورامي", "تراس ساحلي مع أطباق فاخرة وموسمية", "wellness"),
            "room_service": ("خدمة الغرف على مدار الساعة", "ضيافة فاخرة تصلك إلى غرفتك طوال اليوم", "connectivity"),
            "city_tour": ("مكتب الجولات السياحية", "رحلات محلية مخصصة مع مرشدين خاصين", "concierge"),
            "fitness_center": ("نادي اللياقة البانورامي", "أحدث أجهزة اللياقة متاحة ٢٤ ساعة", "wellness"),
            "valet_parking": ("خدمة صف السيارات المجانية", "مواقف داخلية آمنة مع شحن السيارات الكهربائية", "concierge"),
        },
        # Tab 2
        "booking_title": "حجز الغرف الذكي وخدمات الضيوف",
        "booking_subtitle": "اختر نوع الغرفة وتواريخ الإقامة والخدمات الإضافية لمعاينة التكلفة التقديرية فوراً.",
        "booking_step_stay": "١. تواريخ الإقامة والغرفة والخدمات الإضافية",
        "booking_step_guest": "٢. بيانات الضيف وتأكيد طلب الحجز",
        "checkin_date": "تاريخ الوصول",
        "checkout_date": "تاريخ المغادرة",
        "room_type": "نوع الغرفة وتوزيع الأسرّة",
        "num_guests": "عدد الضيوف",
        "extra_services": "الخدمات الإضافية المميزة",
        "guest_name": "الاسم الكامل للضيف *",
        "guest_name_ph": "مثال: عمر المنصور",
        "guest_phone": "رقم الهاتف / واتساب *",
        "guest_phone_ph": "مثال: +971 50 123 4567",
        "guest_email": "البريد الإلكتروني *",
        "guest_email_ph": "مثال: guest@example.com",
        "special_notes": "ملاحظات وطلبات خاصة",
        "special_notes_ph": "تفضيلات الطعام، رقم الرحلة، طلب سرير أطفال أو تجهيز مناسبة خاصة...",
        "submit_booking_btn": "تأكيد طلب الحجز",
        "rooms": {
            "single": "غرفة مفردة (سرير مفرد واحد)",
            "double": "غرفة مزدوجة دبل (سرير كينغ واحد)",
            "twin": "غرفة توين (سريران مفردان)",
            "junior_suite": "جناح جونيور (سرير كينغ + صالة)",
            "royal_suite": "الجناح الملكي العائلي (غرفتا نوم)",
        },
        "guests": {
            "1_adult": "بالغ واحد",
            "2_adults": "شخصان بالغان",
            "2_adults_1_child": "شخصان بالغان + طفل",
            "family_group": "عائلة / مجموعة (٤ أشخاص فأكثر)",
        },
        "services": {
            "airport_vip": "استقبال وتوصيل المطار VIP",
            "breakfast": "شامل الإفطار (لكل ليلة)",
            "late_checkout": "مغادرة متأخرة (حتى ٤:٠٠ عصراً)",
            "spa_massage": "باقة السبا والمساج",
            "honeymoon_decor": "تجهيز غرفة شهر العسل",
        },
        "estimate_title": "ملخص الإقامة والتكلفة التقديرية الفورية",
        "estimate_nights": "مدة الإقامة",
        "estimate_nights_val": "{n} ليلة",
        "estimate_room_rate": "سعر الليلة الواحدة",
        "estimate_room_subtotal": "إجمالي الإقامة",
        "estimate_services_subtotal": "إجمالي الخدمات الإضافية",
        "estimate_total": "الإجمالي التقديري",
        "estimate_per_night": "/ ليلة",
        "estimate_invalid_dates": "يجب أن يكون تاريخ المغادرة بعد تاريخ الوصول بيوم واحد على الأقل.",
        "val_missing_fields": "يرجى إدخال الاسم الكامل ورقم الهاتف والبريد الإلكتروني قبل الإرسال.",
        "val_invalid_email": "يرجى إدخال عنوان بريد إلكتروني صحيح.",
        "val_invalid_dates": "يجب أن يكون تاريخ المغادرة بعد تاريخ الوصول.",
        "booking_confirmed_title": "تم تسجيل طلب الحجز بنجاح",
        "booking_confirmed_desc": "شكراً لك {name}. استلم مكتب الحجوزات طلبك وسيتواصل معك فريقنا قريباً.",
        "booking_ref_label": "رمز مرجع الحجز",
        "booking_summary_line": "{room} · {nights} ليلة · الإجمالي التقديري: {currency} {total:,.0f}",
        # Tab 3
        "ai_title": "مساعد الاستقبال والكونسيرج الذكي",
        "ai_subtitle": "اسأل عن الغرف والأسعار والمرافق ومواعيد التسجيل أو اطلب توصية مخصصة لإقامتك.",
        "ai_welcome": "مرحباً بكم في {hotel}. أنا مساعد الكونسيرج الذكي الخاص بكم. كيف يمكنني مساعدتكم اليوم؟",
        "ai_quick_prompts_label": "أسئلة مقترحة",
        "ai_quick_prompts": [
            "ما أنواع الغرف المتوفرة وما أسعار الليلة؟",
            "أخبرني عن مرافق الفندق ومواعيد الوصول والمغادرة.",
            "ساعدني في اختيار أفضل جناح لعائلة مع خدمات السبا.",
        ],
        "ai_input_placeholder": "اسأل مساعد الاستقبال الذكي أي سؤال حول إقامتك...",
        "ai_clear_chat": "مسح المحادثة",
        "ai_thinking": "جارٍ التواصل مع مكتب الكونسيرج الذكي...",
        "ai_missing_key_error": "مفتاح Gemini API غير مضبوط بعد. يرجى إضافة GEMINI_API_KEY في أسرار Streamlit أو إدخاله في الشريط الجانبي.",
        "ai_api_error": "حدث خطأ مؤقت أثناء الاتصال بالمساعد الذكي. يرجى التحقق من مفتاح API أو اسم النموذج في لوحة الإدارة.",
        "ai_system_instruction": (
            "أنت مساعد الاستقبال والكونسيرج الذكي لفندق {hotel_name} الفاخر من فئة خمس نجوم. "
            "قاعدة اللغة الصارمة: يجب عليك الرد باللغة العربية الفصحى الراقية حصراً وبنسبة ١٠٠٪ دون خلط أي كلمات إنجليزية أو فارسية. "
            "اعتمد فقط على بيانات الفندق الحية التالية. وإذا طُلب أمر خارجها فاقترح بلطف التواصل مع الاستقبال عبر {phone} أو {email}. "
            "اجعل ردودك دافئة ومهنية ومختصرة.\n\n"
            "بيانات الفندق الحية:\n{profile}"
        ),
        # Tab 4
        "admin_title": "لوحة إدارة الفندق وتخصيص العلامة التجارية",
        "admin_pin_prompt": "أدخل رمز الإدارة السري لفتح إعدادات الفندق ولوحة الحجوزات",
        "admin_pin_demo_note": "رمز الدخول التجريبي الافتراضي: 1234",
        "admin_pin_label": "رمز الإدارة السري",
        "admin_unlock_btn": "فتح لوحة الإدارة",
        "admin_lock_btn": "قفل اللوحة",
        "admin_wrong_pin": "الرمز السري غير صحيح. يرجى المحاولة مجدداً (الرمز التجريبي: 1234).",
        "admin_section_a": "القسم الأول — تخصيص هوية وبيانات الفندق",
        "admin_section_b": "القسم الثاني — لوحة الحجوزات وإدارة علاقات العملاء",
        "admin_customizer_expand": "فتح إعدادات الهوية، أسعار الغرف، المرافق ونموذج الذكاء الاصطناعي",
        "cfg_names_group": "هوية الفندق باللغات الثلاث",
        "cfg_name_en": "اسم الفندق (الإنجليزية)",
        "cfg_name_fa": "اسم الفندق (الفارسية)",
        "cfg_name_ar": "اسم الفندق (العربية)",
        "cfg_tagline_en": "الشعار (الإنجليزية)",
        "cfg_tagline_fa": "الشعار (الفارسية)",
        "cfg_tagline_ar": "الشعار (العربية)",
        "cfg_desc_en": "الوصف (الإنجليزية)",
        "cfg_desc_fa": "الوصف (الفارسية)",
        "cfg_desc_ar": "الوصف (العربية)",
        "cfg_addr_en": "العنوان (الإنجليزية)",
        "cfg_addr_fa": "العنوان (الفارسية)",
        "cfg_addr_ar": "العنوان (العربية)",
        "cfg_contact_group": "بيانات التواصل والصورة الرئيسية والموقع",
        "cfg_stars": "تصنيف النجوم",
        "cfg_phone": "رقم الهاتف",
        "cfg_email": "البريد الإلكتروني",
        "cfg_checkin": "وقت تسجيل الوصول",
        "cfg_checkout": "وقت تسجيل المغادرة",
        "cfg_currency": "رمز العملة",
        "cfg_hero_url": "رابط صورة الواجهة الرئيسية",
        "cfg_lat": "خط العرض",
        "cfg_lon": "خط الطول",
        "cfg_pricing_group": "أسعار الغرف الأساسية والمرافق المفعلة",
        "cfg_amenities_label": "المرافق المفعلة في الفندق",
        "cfg_ai_group": "إعدادات الذكاء الاصطناعي والأمان",
        "cfg_gemini_model": "اسم نموذج Gemini",
        "cfg_admin_pin": "رمز الإدارة السري",
        "cfg_save_btn": "حفظ إعدادات الفندق",
        "cfg_saved_msg": "تم حفظ إعدادات الفندق في hotel_config.json وتحديث المنصة فوراً.",
        "kpi_total": "إجمالي الطلبات",
        "kpi_pending": "قيد الانتظار",
        "kpi_confirmed": "حجوزات مؤكدة",
        "kpi_revenue": "الإيرادات التقديرية",
        "crm_no_bookings": "لم يتم تسجيل أي طلبات حجز بعد. ستظهر الحجوزات الجديدة من التبويب الثاني هنا تلقائياً.",
        "crm_update_title": "تحديث حالة الحجز",
        "crm_select_booking": "اختر رمز مرجع الحجز",
        "crm_select_status": "الحالة الجديدة",
        "crm_update_btn": "حفظ تحديث الحالة",
        "crm_status_updated": "تم تحديث حالة الحجز {ref} إلى «{status}».",
        "crm_download_csv": "تنزيل جدول الحجوزات (CSV)",
        "statuses": {
            "Pending": "قيد الانتظار",
            "Confirmed": "مؤكد",
            "Completed": "مكتمل",
            "Cancelled": "ملغى",
        },
        "table_cols": {
            "ref_id": "رمز الحجز",
            "created_at": "تاريخ الطلب",
            "guest_name": "اسم الضيف",
            "phone": "الهاتف / واتساب",
            "email": "البريد الإلكتروني",
            "check_in": "الوصول",
            "check_out": "المغادرة",
            "nights": "الليالي",
            "room_type": "نوع الغرفة",
            "guests": "الضيوف",
            "services": "الخدمات الإضافية",
            "estimated_total": "الإجمالي التقديري",
            "status": "الحالة",
            "notes": "ملاحظات",
        },
    },
}


# =============================================================================
# 3. UTF-8 JSON STORAGE INITIALIZATION & HELPERS
# =============================================================================


def _deep_merge_defaults(data: dict[str, Any], defaults: dict[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    for key, val in data.items():
        if isinstance(val, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge_defaults(val, merged[key])
        else:
            merged[key] = val
    return merged


def init_storage() -> None:
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(
            json.dumps(DEFAULT_HOTEL_CONFIG, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    if not BOOKINGS_FILE.exists():
        BOOKINGS_FILE.write_text("[]", encoding="utf-8")


def load_hotel_config() -> dict[str, Any]:
    init_storage()
    try:
        raw = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            return _deep_merge_defaults(raw, DEFAULT_HOTEL_CONFIG)
    except (OSError, json.JSONDecodeError):
        pass
    return json.loads(json.dumps(DEFAULT_HOTEL_CONFIG))


def save_hotel_config(config: dict[str, Any]) -> None:
    CONFIG_FILE.write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_bookings() -> list[dict[str, Any]]:
    init_storage()
    try:
        raw = json.loads(BOOKINGS_FILE.read_text(encoding="utf-8"))
        if isinstance(raw, list):
            return raw
    except (OSError, json.JSONDecodeError):
        pass
    return []


def save_bookings(bookings: list[dict[str, Any]]) -> None:
    BOOKINGS_FILE.write_text(
        json.dumps(bookings, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def generate_booking_ref(existing: list[dict[str, Any]]) -> str:
    year = datetime.date.today().year
    existing_ids = {str(item.get("ref_id", "")) for item in existing}
    for _ in range(100):
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
        candidate = f"HTL-{year}-{code}"
        if candidate not in existing_ids:
            return candidate
    return f"HTL-{year}-{random.randint(1000, 9999)}"


def calculate_stay_estimate(
    config: dict[str, Any],
    room_key: str,
    nights: int,
    service_keys: list[str],
) -> tuple[float, float, float, float]:
    nightly_rate = float(config.get("room_prices", {}).get(room_key, 200))
    valid_nights = max(nights, 0)
    room_subtotal = nightly_rate * valid_nights
    service_prices = config.get("service_prices", {})
    services_subtotal = 0.0
    for svc in service_keys:
        price = float(service_prices.get(svc, 0))
        if svc == "breakfast":
            services_subtotal += price * max(valid_nights, 1)
        else:
            services_subtotal += price
    return nightly_rate, room_subtotal, services_subtotal, room_subtotal + services_subtotal


def resolve_gemini_api_key(override_key: str) -> str:
    if override_key and override_key.strip():
        return override_key.strip()
    try:
        if "GEMINI_API_KEY" in st.secrets and str(st.secrets["GEMINI_API_KEY"]).strip():
            return str(st.secrets["GEMINI_API_KEY"]).strip()
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY", "").strip()


# =============================================================================
# 4. DYNAMIC LUXURY THEME & RTL/LTR CSS INJECTION
# =============================================================================


def inject_luxury_css(lang: str) -> None:
    t = TRANSLATIONS[lang]
    direction = t["dir"]
    align = t["align"]
    font_family = t["font_family"]
    font_import = t["font_import"]

    css = f"""
    <style>
    @import url('{font_import}');

    html, body, [class*="css"], .stApp, .stMarkdown, .stTextInput, .stTextArea,
    .stSelectbox, .stMultiSelect, .stDateInput, .stNumberInput, .stButton,
    .stFormSubmitButton, .stTabs, .stExpander, .stChatMessage, .stAlert,
    section[data-testid="stSidebar"] {{
        font-family: {font_family} !important;
        direction: {direction} !important;
        text-align: {align} !important;
    }}

    .stApp {{
        background-color: #FAF9F4;
        background-image:
            radial-gradient(at 8% 12%, rgba(167, 215, 145, 0.42) 0px, transparent 52%),
            radial-gradient(at 92% 10%, rgba(253, 186, 116, 0.38) 0px, transparent 50%),
            radial-gradient(at 84% 86%, rgba(183, 224, 162, 0.36) 0px, transparent 54%),
            radial-gradient(at 14% 88%, rgba(254, 205, 155, 0.36) 0px, transparent 52%),
            linear-gradient(135deg, #F1F8EC 0%, #FFFBF5 50%, #FFF1E2 100%);
        background-attachment: fixed;
        color: #0F172A;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        border-inline-end: 1px solid rgba(217, 119, 6, 0.25);
        padding-top: 0.75rem;
    }}

    section[data-testid="stSidebar"] * {{
        color: #F8FAFC !important;
    }}

    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {{
        background-color: rgba(15, 23, 42, 0.78) !important;
        border: 1px solid rgba(217, 119, 6, 0.45) !important;
        color: #F8FAFC !important;
        border-radius: 10px !important;
    }}

    [data-baseweb="popover"], [data-baseweb="menu"], ul[role="listbox"] {{
        direction: {direction} !important;
        text-align: {align} !important;
        font-family: {font_family} !important;
    }}

    .stButton > button,
    .stFormSubmitButton > button,
    .stDownloadButton > button {{
        background: linear-gradient(135deg, #D97706 0%, #B45309 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 0.62rem 1.35rem !important;
        box-shadow: 0 4px 12px rgba(217, 119, 6, 0.25) !important;
        transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease !important;
    }}

    .stButton > button:hover,
    .stFormSubmitButton > button:hover,
    .stDownloadButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 18px rgba(180, 83, 9, 0.35) !important;
        filter: brightness(1.05) !important;
    }}

    div[data-testid="stForm"] {{
        background: rgba(255, 255, 255, 0.94);
        border: 1px solid rgba(132, 169, 120, 0.28);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.04);
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(132, 169, 120, 0.28);
        border-radius: 12px;
        padding: 0.35rem;
        margin-bottom: 0.6rem;
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 9px !important;
        padding: 0.6rem 1.15rem !important;
        font-weight: 600 !important;
        color: #475569 !important;
        background: transparent !important;
    }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%) !important;
        color: #FDE68A !important;
    }}

    .luxury-hero {{
        position: relative;
        width: 100%;
        min-height: 295px;
        border-radius: 18px;
        overflow: hidden;
        background-color: #0F172A;
        margin-bottom: 1.35rem;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.18);
        border: 1px solid rgba(217, 119, 6, 0.32);
    }}

    .luxury-hero-bg {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: 0;
    }}

    .luxury-hero-overlay {{
        position: relative;
        z-index: 2;
        min-height: 295px;
        padding: 2rem 2.25rem;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        background: linear-gradient(
            180deg,
            rgba(15, 23, 42, 0.22) 0%,
            rgba(15, 23, 42, 0.68) 52%,
            rgba(15, 23, 42, 0.93) 100%
        );
    }}

    .luxury-stars {{
        display: inline-block;
        width: fit-content;
        padding: 0.32rem 0.88rem;
        border-radius: 8px;
        background: rgba(217, 119, 6, 0.95);
        color: #FFFFFF;
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }}

    .luxury-hero-title {{
        color: #FFFFFF;
        font-size: 2.15rem;
        font-weight: 700;
        margin: 0 0 0.4rem 0;
        line-height: 1.25;
    }}

    .luxury-hero-tagline {{
        color: #E2E8F0;
        font-size: 1.05rem;
        margin: 0 0 1.15rem 0;
        max-width: 780px;
    }}

    .luxury-hero-meta {{
        display: flex;
        flex-wrap: wrap;
        gap: 1.25rem;
        color: #FDE68A;
        font-size: 0.88rem;
        font-weight: 500;
        border-top: 1px solid rgba(255, 255, 255, 0.18);
        padding-top: 0.85rem;
    }}

    .luxury-card {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.25rem 1.35rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
    }}

    .amenity-card {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1rem 1.15rem;
        height: 100%;
        margin-bottom: 0.75rem;
    }}

    .amenity-cat {{
        color: #B45309;
        font-size: 0.76rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }}

    .amenity-title {{
        color: #0F172A;
        font-size: 0.98rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }}

    .amenity-desc {{
        color: #475569;
        font-size: 0.86rem;
        line-height: 1.5;
    }}

    .estimate-box {{
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #F8FAFC;
        border-radius: 14px;
        padding: 1.35rem 1.5rem;
        border: 1px solid rgba(217, 119, 6, 0.45);
        margin-bottom: 1.2rem;
    }}

    .estimate-row {{
        display: flex;
        justify-content: space-between;
        padding: 0.35rem 0;
        font-size: 0.93rem;
        color: #CBD5E1;
    }}

    .estimate-total-row {{
        display: flex;
        justify-content: space-between;
        padding-top: 0.75rem;
        margin-top: 0.6rem;
        border-top: 1px solid rgba(255, 255, 255, 0.18);
        font-size: 1.18rem;
        font-weight: 700;
        color: #FDE68A;
    }}

    .confirm-banner {{
        background: linear-gradient(135deg, #064E3B 0%, #065F46 100%);
        color: #ECFDF5;
        border-radius: 16px;
        padding: 1.5rem 1.75rem;
        margin: 1rem 0;
        border: 1px solid #10B981;
    }}

    .confirm-code {{
        display: inline-block;
        background: rgba(255, 255, 255, 0.14);
        border: 1px dashed #6EE7B7;
        border-radius: 10px;
        padding: 0.45rem 1rem;
        font-family: monospace !important;
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #FFFFFF;
        margin: 0.5rem 0;
        direction: ltr !important;
    }}

    [data-testid="stChatMessage"] {{
        direction: {direction} !important;
        text-align: {align} !important;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.65rem;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# =============================================================================
# 5. UI COMPONENTS: HERO BANNER & FOUR CORE TABS
# =============================================================================


def render_hero_banner(config: dict[str, Any], lang: str) -> None:
    t = TRANSLATIONS[lang]
    hotel_name = html.escape(str(config["name"].get(lang, config["name"]["en"])))
    tagline = html.escape(str(config["tagline"].get(lang, config["tagline"]["en"])))
    phone = html.escape(str(config.get("phone", "")))
    email = html.escape(str(config.get("email", "")))
    check_in = html.escape(str(config.get("check_in_time", "15:00")))
    check_out = html.escape(str(config.get("check_out_time", "12:00")))
    stars = int(config.get("star_rating", 5))
    star_icons = "★" * max(1, min(stars, 5))
    star_text = html.escape(t["star_badge"].format(stars=stars))
    hero_url = html.escape(str(config.get("hero_image_url") or DEFAULT_HERO_IMAGE))
    fallback_url = html.escape(DEFAULT_HERO_IMAGE)

    hero_html = f"""
    <div class="luxury-hero">
        <img
            class="luxury-hero-bg"
            src="{hero_url}"
            alt="{hotel_name}"
            onerror="this.onerror=null;this.src='{fallback_url}';"
        />
        <div class="luxury-hero-overlay">
            <div class="luxury-stars">{star_icons} &nbsp; {star_text}</div>
            <h1 class="luxury-hero-title">{hotel_name}</h1>
            <p class="luxury-hero-tagline">{tagline}</p>
            <div class="luxury-hero-meta">
                <span>{t['sidebar_phone']}: <bdi>{phone}</bdi></span>
                <span>{t['sidebar_email']}: <bdi>{email}</bdi></span>
                <span>{t['hero_checkin_label']}: <bdi>{check_in}</bdi> · {t['hero_checkout_label']}: <bdi>{check_out}</bdi></span>
            </div>
        </div>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)


def render_overview_tab(config: dict[str, Any], lang: str) -> None:
    t = TRANSLATIONS[lang]
    description = html.escape(str(config["description"].get(lang, config["description"]["en"])))
    address = html.escape(str(config["address"].get(lang, config["address"]["en"])))
    phone = html.escape(str(config.get("phone", "")))
    email = html.escape(str(config.get("email", "")))
    check_in = html.escape(str(config.get("check_in_time", "15:00")))
    check_out = html.escape(str(config.get("check_out_time", "12:00")))
    lat = float(config.get("latitude", 25.2048))
    lon = float(config.get("longitude", 55.2708))

    col_info, col_map = st.columns([1.15, 1.0], gap="large")

    with col_info:
        st.subheader(t["overview_about_title"])
        st.markdown(
            f"""
            <div class="luxury-card">
                <p style="margin:0; line-height:1.85; color:#334155; font-size:0.98rem;">{description}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.subheader(t["overview_details_title"])
        st.markdown(
            f"""
            <div class="luxury-card">
                <div style="margin-bottom:0.65rem;">
                    <div style="color:#B45309; font-size:0.8rem; font-weight:700;">{t['overview_address_label']}</div>
                    <div style="color:#0F172A; font-weight:600;">{address}</div>
                </div>
                <div style="margin-bottom:0.65rem;">
                    <div style="color:#B45309; font-size:0.8rem; font-weight:700;">{t['overview_phone_label']}</div>
                    <div style="color:#0F172A; font-weight:600;"><bdi>{phone}</bdi></div>
                </div>
                <div style="margin-bottom:0.65rem;">
                    <div style="color:#B45309; font-size:0.8rem; font-weight:700;">{t['overview_email_label']}</div>
                    <div style="color:#0F172A; font-weight:600;"><bdi>{email}</bdi></div>
                </div>
                <div>
                    <div style="color:#B45309; font-size:0.8rem; font-weight:700;">{t['overview_hours_label']}</div>
                    <div style="color:#0F172A; font-weight:600;">{t['hero_checkin_label']}: <bdi>{check_in}</bdi> &nbsp;|&nbsp; {t['hero_checkout_label']}: <bdi>{check_out}</bdi></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_map:
        st.subheader(t["overview_map_title"])
        map_df = pd.DataFrame({"lat": [lat], "lon": [lon]})
        st.map(map_df, zoom=13)
        st.caption(t["overview_map_caption"].format(lat=lat, lon=lon))

    st.divider()
    st.subheader(t["overview_amenities_title"])
    active_amenities = [
        key for key in config.get("active_amenities", AMENITY_KEYS) if key in t["amenities"]
    ]

    if not active_amenities:
        st.info(t["overview_amenities_empty"])
    else:
        cols = st.columns(4, gap="medium")
        for idx, amenity_key in enumerate(active_amenities):
            title, desc, cat_key = t["amenities"][amenity_key]
            cat_label = t["amenity_categories"].get(cat_key, "")
            with cols[idx % 4]:
                st.markdown(
                    f"""
                    <div class="amenity-card">
                        <div class="amenity-cat">{html.escape(cat_label)}</div>
                        <div class="amenity-title">{html.escape(title)}</div>
                        <div class="amenity-desc">{html.escape(desc)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def render_booking_tab(config: dict[str, Any], lang: str) -> None:
    t = TRANSLATIONS[lang]
    currency = str(config.get("currency", "USD"))

    st.subheader(t["booking_title"])
    st.write(t["booking_subtitle"])

    st.markdown(f"#### {t['booking_step_stay']}")
    today = datetime.date.today()
    default_checkout = today + datetime.timedelta(days=2)

    col_stay, col_preview = st.columns([1.3, 1.0], gap="large")

    with col_stay:
        c_in, c_out = st.columns(2)
        with c_in:
            check_in_date = st.date_input(
                t["checkin_date"],
                value=today,
                min_value=today,
                key="booking_check_in",
            )
        with c_out:
            check_out_date = st.date_input(
                t["checkout_date"],
                value=max(default_checkout, check_in_date + datetime.timedelta(days=1)),
                min_value=today + datetime.timedelta(days=1),
                key="booking_check_out",
            )

        room_key = st.selectbox(
            t["room_type"],
            options=ROOM_KEYS,
            format_func=lambda k: (
                f"{t['rooms'][k]} — {currency} {config['room_prices'].get(k, 200):,.0f} {t['estimate_per_night']}"
            ),
            key="booking_room_type",
        )

        guest_key = st.selectbox(
            t["num_guests"],
            options=GUEST_KEYS,
            format_func=lambda k: t["guests"][k],
            key="booking_guests",
        )

        selected_services = st.multiselect(
            t["extra_services"],
            options=SERVICE_KEYS,
            format_func=lambda k: (
                f"{t['services'][k]} (+{currency} {config['service_prices'].get(k, 0):,.0f})"
            ),
            key="booking_services",
        )

    nights = (check_out_date - check_in_date).days
    nightly_rate, room_sub, svc_sub, grand_total = calculate_stay_estimate(
        config, room_key, max(nights, 0), selected_services
    )

    with col_preview:
        if nights <= 0:
            st.warning(t["estimate_invalid_dates"])
        else:
            nights_display = html.escape(t["estimate_nights_val"].format(n=nights))
            room_label = html.escape(t["rooms"][room_key])
            st.markdown(
                f"""
                <div class="estimate-box">
                    <div style="font-size:1.05rem; font-weight:700; color:#FFFFFF; margin-bottom:0.85rem;">
                        {html.escape(t['estimate_title'])}
                    </div>
                    <div class="estimate-row">
                        <span>{html.escape(t['room_type'])}</span>
                        <span><strong>{room_label}</strong></span>
                    </div>
                    <div class="estimate-row">
                        <span>{html.escape(t['estimate_nights'])}</span>
                        <span>{nights_display}</span>
                    </div>
                    <div class="estimate-row">
                        <span>{html.escape(t['estimate_room_rate'])}</span>
                        <span><bdi>{currency} {nightly_rate:,.0f}</bdi></span>
                    </div>
                    <div class="estimate-row">
                        <span>{html.escape(t['estimate_room_subtotal'])}</span>
                        <span><bdi>{currency} {room_sub:,.0f}</bdi></span>
                    </div>
                    <div class="estimate-row">
                        <span>{html.escape(t['estimate_services_subtotal'])}</span>
                        <span><bdi>{currency} {svc_sub:,.0f}</bdi></span>
                    </div>
                    <div class="estimate-total-row">
                        <span>{html.escape(t['estimate_total'])}</span>
                        <span><bdi>{currency} {grand_total:,.0f}</bdi></span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(f"#### {t['booking_step_guest']}")
    with st.form("guest_booking_form", clear_on_submit=False):
        g_col1, g_col2, g_col3 = st.columns(3)
        with g_col1:
            guest_name = st.text_input(t["guest_name"], placeholder=t["guest_name_ph"])
        with g_col2:
            guest_phone = st.text_input(t["guest_phone"], placeholder=t["guest_phone_ph"])
        with g_col3:
            guest_email = st.text_input(t["guest_email"], placeholder=t["guest_email_ph"])

        special_notes = st.text_area(
            t["special_notes"],
            placeholder=t["special_notes_ph"],
            height=95,
        )

        submitted = st.form_submit_button(t["submit_booking_btn"], width="stretch")

    if submitted:
        if not guest_name.strip() or not guest_phone.strip() or not guest_email.strip():
            st.error(t["val_missing_fields"])
            return
        if "@" not in guest_email or "." not in guest_email.split("@")[-1]:
            st.error(t["val_invalid_email"])
            return
        if nights <= 0:
            st.error(t["val_invalid_dates"])
            return

        bookings = load_bookings()
        ref_id = generate_booking_ref(bookings)
        new_record = {
            "ref_id": ref_id,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "guest_name": guest_name.strip(),
            "phone": guest_phone.strip(),
            "email": guest_email.strip(),
            "check_in": check_in_date.isoformat(),
            "check_out": check_out_date.isoformat(),
            "nights": nights,
            "room_type": room_key,
            "guests": guest_key,
            "services": list(selected_services),
            "estimated_total": round(grand_total, 2),
            "currency": currency,
            "status": "Pending",
            "notes": special_notes.strip(),
            "language": lang,
        }
        bookings.insert(0, new_record)
        save_bookings(bookings)
        st.session_state["last_confirmed_booking"] = new_record

    if "last_confirmed_booking" in st.session_state:
        rec = st.session_state["last_confirmed_booking"]
        room_display = t["rooms"].get(rec["room_type"], rec["room_type"])
        summary_line = t["booking_summary_line"].format(
            room=room_display,
            nights=rec["nights"],
            currency=rec.get("currency", currency),
            total=float(rec.get("estimated_total", 0)),
        )
        desc_line = t["booking_confirmed_desc"].format(name=rec["guest_name"])
        st.markdown(
            f"""
            <div class="confirm-banner">
                <div style="font-size:1.2rem; font-weight:700; margin-bottom:0.35rem;">
                    {html.escape(t['booking_confirmed_title'])}
                </div>
                <p style="margin:0 0 0.7rem 0; color:#D1FAE5;">{html.escape(desc_line)}</p>
                <div style="font-size:0.82rem; color:#A7F3D0;">{html.escape(t['booking_ref_label'])}</div>
                <div class="confirm-code">{html.escape(rec['ref_id'])}</div>
                <div style="font-size:0.92rem; margin-top:0.5rem; color:#ECFDF5;">{html.escape(summary_line)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _build_hotel_profile_for_ai(config: dict[str, Any], lang: str) -> str:
    t = TRANSLATIONS[lang]
    currency = str(config.get("currency", "USD"))
    rooms_lines = [
        f"- {t['rooms'][k]}: {currency} {config['room_prices'].get(k, 200):,.0f} {t['estimate_per_night']}"
        for k in ROOM_KEYS
    ]
    services_lines = [
        f"- {t['services'][k]}: {currency} {config['service_prices'].get(k, 0):,.0f}"
        for k in SERVICE_KEYS
    ]
    amenities_lines = [
        f"- {t['amenities'][k][0]}: {t['amenities'][k][1]}"
        for k in config.get("active_amenities", [])
        if k in t["amenities"]
    ]
    return (
        f"Hotel Name: {config['name'].get(lang, config['name']['en'])}\n"
        f"Star Rating: {config.get('star_rating', 5)}\n"
        f"Tagline: {config['tagline'].get(lang, config['tagline']['en'])}\n"
        f"Description: {config['description'].get(lang, config['description']['en'])}\n"
        f"Address: {config['address'].get(lang, config['address']['en'])}\n"
        f"Phone: {config.get('phone', '')}\n"
        f"Email: {config.get('email', '')}\n"
        f"Check-in: {config.get('check_in_time', '15:00')} | Check-out: {config.get('check_out_time', '12:00')}\n"
        f"Rooms & Nightly Rates:\n" + "\n".join(rooms_lines) + "\n"
        f"Extra Guest Services:\n" + "\n".join(services_lines) + "\n"
        f"Amenities:\n" + "\n".join(amenities_lines)
    )


def _query_gemini_concierge(
    api_key: str,
    model_name: str,
    config: dict[str, Any],
    lang: str,
    history: list[dict[str, str]],
) -> str:
    t = TRANSLATIONS[lang]
    hotel_name = str(config["name"].get(lang, config["name"]["en"]))
    profile = _build_hotel_profile_for_ai(config, lang)
    system_instruction = t["ai_system_instruction"].format(
        hotel_name=hotel_name,
        phone=config.get("phone", ""),
        email=config.get("email", ""),
        profile=profile,
    )

    client = genai.Client(api_key=api_key)
    contents: list[types.Content] = []
    for msg in history[-12:]:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
        )

    response = client.models.generate_content(
        model=model_name or GEMINI_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
        ),
    )
    return (response.text or "").strip()


def render_ai_concierge_tab(config: dict[str, Any], lang: str, api_key: str) -> None:
    t = TRANSLATIONS[lang]
    hotel_name = str(config["name"].get(lang, config["name"]["en"]))
    model_name = str(config.get("gemini_model") or GEMINI_MODEL)

    head_col, clear_col = st.columns([4, 1])
    with head_col:
        st.subheader(t["ai_title"])
        st.write(t["ai_subtitle"])
    with clear_col:
        if st.button(t["ai_clear_chat"], key="clear_concierge_chat", width="stretch"):
            st.session_state[f"chat_history_{lang}"] = []
            st.rerun()

    chat_key = f"chat_history_{lang}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []

    with st.chat_message("assistant"):
        st.markdown(t["ai_welcome"].format(hotel=hotel_name))

    for message in st.session_state[chat_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.caption(t["ai_quick_prompts_label"])
    prompt_cols = st.columns(3, gap="small")
    clicked_prompt: str | None = None
    for idx, quick_text in enumerate(t["ai_quick_prompts"]):
        with prompt_cols[idx]:
            if st.button(quick_text, key=f"quick_prompt_{lang}_{idx}", width="stretch"):
                clicked_prompt = quick_text

    typed_prompt = st.chat_input(t["ai_input_placeholder"], key=f"chat_input_{lang}")
    active_prompt = clicked_prompt or typed_prompt

    if active_prompt:
        st.session_state[chat_key].append({"role": "user", "content": active_prompt})
        with st.chat_message("user"):
            st.markdown(active_prompt)

        if not api_key:
            st.warning(t["ai_missing_key_error"])
            return

        with st.chat_message("assistant"):
            with st.spinner(t["ai_thinking"]):
                try:
                    reply = _query_gemini_concierge(
                        api_key=api_key,
                        model_name=model_name,
                        config=config,
                        lang=lang,
                        history=st.session_state[chat_key],
                    )
                    if not reply:
                        reply = t["ai_api_error"]
                    st.markdown(reply)
                    st.session_state[chat_key].append({"role": "assistant", "content": reply})
                except Exception:
                    st.error(t["ai_api_error"])


def render_admin_tab(config: dict[str, Any], lang: str) -> None:
    t = TRANSLATIONS[lang]
    st.subheader(t["admin_title"])

    if "admin_unlocked" not in st.session_state:
        st.session_state["admin_unlocked"] = False

    if not st.session_state["admin_unlocked"]:
        st.info(f"{t['admin_pin_prompt']} — {t['admin_pin_demo_note']}")
        with st.form("admin_pin_gate"):
            pin_input = st.text_input(t["admin_pin_label"], type="password")
            unlock_clicked = st.form_submit_button(t["admin_unlock_btn"], width="stretch")
        if unlock_clicked:
            expected_pin = str(config.get("admin_pin", "1234"))
            if pin_input.strip() == expected_pin:
                st.session_state["admin_unlocked"] = True
                st.rerun()
            else:
                st.error(t["admin_wrong_pin"])
        return

    top_bar1, top_bar2 = st.columns([5, 1])
    with top_bar1:
        st.markdown(f"### {t['admin_section_b']}")
    with top_bar2:
        if st.button(t["admin_lock_btn"], key="lock_admin_btn", width="stretch"):
            st.session_state["admin_unlocked"] = False
            st.rerun()

    # -------------------------------------------------------------------------
    # SECTION B — BOOKINGS & CRM DASHBOARD
    # -------------------------------------------------------------------------
    bookings = load_bookings()
    currency = str(config.get("currency", "USD"))

    total_count = len(bookings)
    pending_count = sum(1 for b in bookings if b.get("status") == "Pending")
    confirmed_count = sum(1 for b in bookings if b.get("status") == "Confirmed")
    est_revenue = sum(
        float(b.get("estimated_total", 0))
        for b in bookings
        if b.get("status") != "Cancelled"
    )

    k1, k2, k3, k4 = st.columns(4)
    k1.metric(t["kpi_total"], f"{total_count}")
    k2.metric(t["kpi_pending"], f"{pending_count}")
    k3.metric(t["kpi_confirmed"], f"{confirmed_count}")
    k4.metric(t["kpi_revenue"], f"{currency} {est_revenue:,.0f}")

    if not bookings:
        st.info(t["crm_no_bookings"])
    else:
        col_map = t["table_cols"]
        display_rows = []
        for b in bookings:
            svc_labels = [
                t["services"].get(s, s) for s in b.get("services", [])
            ]
            display_rows.append(
                {
                    col_map["ref_id"]: b.get("ref_id", ""),
                    col_map["created_at"]: b.get("created_at", ""),
                    col_map["guest_name"]: b.get("guest_name", ""),
                    col_map["phone"]: b.get("phone", ""),
                    col_map["email"]: b.get("email", ""),
                    col_map["check_in"]: b.get("check_in", ""),
                    col_map["check_out"]: b.get("check_out", ""),
                    col_map["nights"]: b.get("nights", 0),
                    col_map["room_type"]: t["rooms"].get(b.get("room_type", ""), b.get("room_type", "")),
                    col_map["guests"]: t["guests"].get(b.get("guests", ""), b.get("guests", "")),
                    col_map["services"]: ", ".join(svc_labels),
                    col_map["estimated_total"]: f"{b.get('currency', currency)} {float(b.get('estimated_total', 0)):,.0f}",
                    col_map["status"]: t["statuses"].get(b.get("status", "Pending"), b.get("status", "Pending")),
                    col_map["notes"]: b.get("notes", ""),
                }
            )

        df = pd.DataFrame(display_rows)
        st.dataframe(df, width="stretch", hide_index=True)

        st.markdown(f"#### {t['crm_update_title']}")
        u1, u2, u3 = st.columns([1.4, 1.2, 1.0])
        ref_options = [b["ref_id"] for b in bookings]
        with u1:
            target_ref = st.selectbox(t["crm_select_booking"], options=ref_options)
        current_booking = next((b for b in bookings if b["ref_id"] == target_ref), bookings[0])
        current_status = current_booking.get("status", "Pending")
        status_idx = STATUS_KEYS.index(current_status) if current_status in STATUS_KEYS else 0
        with u2:
            new_status = st.selectbox(
                t["crm_select_status"],
                options=STATUS_KEYS,
                index=status_idx,
                format_func=lambda s: t["statuses"][s],
            )
        with u3:
            st.markdown("<div style='height:1.72rem;'></div>", unsafe_allow_html=True)
            if st.button(t["crm_update_btn"], key="update_status_btn", width="stretch"):
                for b in bookings:
                    if b["ref_id"] == target_ref:
                        b["status"] = new_status
                        break
                save_bookings(bookings)
                st.success(
                    t["crm_status_updated"].format(
                        ref=target_ref,
                        status=t["statuses"][new_status],
                    )
                )
                st.rerun()

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_bytes = ("\ufeff" + csv_buffer.getvalue()).encode("utf-8")
        st.download_button(
            label=t["crm_download_csv"],
            data=csv_bytes,
            file_name=f"hotel_bookings_{datetime.date.today().isoformat()}.csv",
            mime="text/csv",
            width="stretch",
        )

    st.divider()

    # -------------------------------------------------------------------------
    # SECTION A — WHITE-LABEL HOTEL CUSTOMIZER (IN EXPANDER FOR CLEAN DEMO)
    # -------------------------------------------------------------------------
    st.markdown(f"### {t['admin_section_a']}")
    with st.expander(t["admin_customizer_expand"], expanded=False):
        with st.form("white_label_config_form"):
            st.markdown(f"**{t['cfg_names_group']}**")
            n1, n2, n3 = st.columns(3)
            with n1:
                name_en = st.text_input(t["cfg_name_en"], value=config["name"].get("en", ""))
                tagline_en = st.text_input(t["cfg_tagline_en"], value=config["tagline"].get("en", ""))
                addr_en = st.text_input(t["cfg_addr_en"], value=config["address"].get("en", ""))
                desc_en = st.text_area(t["cfg_desc_en"], value=config["description"].get("en", ""), height=90)
            with n2:
                name_fa = st.text_input(t["cfg_name_fa"], value=config["name"].get("fa", ""))
                tagline_fa = st.text_input(t["cfg_tagline_fa"], value=config["tagline"].get("fa", ""))
                addr_fa = st.text_input(t["cfg_addr_fa"], value=config["address"].get("fa", ""))
                desc_fa = st.text_area(t["cfg_desc_fa"], value=config["description"].get("fa", ""), height=90)
            with n3:
                name_ar = st.text_input(t["cfg_name_ar"], value=config["name"].get("ar", ""))
                tagline_ar = st.text_input(t["cfg_tagline_ar"], value=config["tagline"].get("ar", ""))
                addr_ar = st.text_input(t["cfg_addr_ar"], value=config["address"].get("ar", ""))
                desc_ar = st.text_area(t["cfg_desc_ar"], value=config["description"].get("ar", ""), height=90)

            st.markdown(f"**{t['cfg_contact_group']}**")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                star_rating = st.slider(
                    t["cfg_stars"],
                    min_value=1,
                    max_value=5,
                    value=int(config.get("star_rating", 5)),
                )
                currency_code = st.text_input(t["cfg_currency"], value=str(config.get("currency", "USD")))
            with c2:
                phone = st.text_input(t["cfg_phone"], value=str(config.get("phone", "")))
                check_in_time = st.text_input(t["cfg_checkin"], value=str(config.get("check_in_time", "15:00")))
            with c3:
                email = st.text_input(t["cfg_email"], value=str(config.get("email", "")))
                check_out_time = st.text_input(t["cfg_checkout"], value=str(config.get("check_out_time", "12:00")))
            with c4:
                lat = st.number_input(
                    t["cfg_lat"],
                    value=float(config.get("latitude", 25.2048)),
                    format="%.6f",
                )
                lon = st.number_input(
                    t["cfg_lon"],
                    value=float(config.get("longitude", 55.2708)),
                    format="%.6f",
                )

            hero_url = st.text_input(
                t["cfg_hero_url"],
                value=str(config.get("hero_image_url", DEFAULT_HERO_IMAGE)),
            )

            st.markdown(f"**{t['cfg_pricing_group']}**")
            p_cols = st.columns(len(ROOM_KEYS))
            updated_room_prices: dict[str, float] = {}
            for idx, rk in enumerate(ROOM_KEYS):
                with p_cols[idx]:
                    updated_room_prices[rk] = float(
                        st.number_input(
                            t["rooms"][rk],
                            min_value=10.0,
                            value=float(config.get("room_prices", {}).get(rk, 200)),
                            step=10.0,
                        )
                    )

            active_amenities = st.multiselect(
                t["cfg_amenities_label"],
                options=AMENITY_KEYS,
                default=[a for a in config.get("active_amenities", AMENITY_KEYS) if a in AMENITY_KEYS],
                format_func=lambda k: t["amenities"][k][0],
            )

            st.markdown(f"**{t['cfg_ai_group']}**")
            ai_c1, ai_c2 = st.columns(2)
            with ai_c1:
                gemini_model = st.text_input(
                    t["cfg_gemini_model"],
                    value=str(config.get("gemini_model", GEMINI_MODEL)),
                )
            with ai_c2:
                admin_pin = st.text_input(
                    t["cfg_admin_pin"],
                    value=str(config.get("admin_pin", "1234")),
                    type="password",
                )

            save_cfg = st.form_submit_button(t["cfg_save_btn"], width="stretch")

    if save_cfg:
        new_config = dict(config)
        new_config["name"] = {"en": name_en.strip(), "fa": name_fa.strip(), "ar": name_ar.strip()}
        new_config["tagline"] = {
            "en": tagline_en.strip(),
            "fa": tagline_fa.strip(),
            "ar": tagline_ar.strip(),
        }
        new_config["description"] = {
            "en": desc_en.strip(),
            "fa": desc_fa.strip(),
            "ar": desc_ar.strip(),
        }
        new_config["address"] = {
            "en": addr_en.strip(),
            "fa": addr_fa.strip(),
            "ar": addr_ar.strip(),
        }
        new_config["star_rating"] = int(star_rating)
        new_config["phone"] = phone.strip()
        new_config["email"] = email.strip()
        new_config["check_in_time"] = check_in_time.strip()
        new_config["check_out_time"] = check_out_time.strip()
        new_config["currency"] = currency_code.strip() or "USD"
        new_config["hero_image_url"] = hero_url.strip() or DEFAULT_HERO_IMAGE
        new_config["latitude"] = float(lat)
        new_config["longitude"] = float(lon)
        new_config["room_prices"] = updated_room_prices
        new_config["active_amenities"] = list(active_amenities)
        new_config["gemini_model"] = gemini_model.strip() or GEMINI_MODEL
        new_config["admin_pin"] = admin_pin.strip() or "1234"

        save_hotel_config(new_config)
        st.success(t["cfg_saved_msg"])
        st.rerun()


# =============================================================================
# 6. MAIN APPLICATION ENTRYPOINT
# =============================================================================


def main() -> None:
    st.set_page_config(
        page_title="Aurelia Grand — Hotel CRM & AI Guest Concierge",
        page_icon="🏨",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_storage()
    config = load_hotel_config()

    if "lang" not in st.session_state:
        st.session_state["lang"] = "en"

    with st.sidebar:
        selected_lang = st.selectbox(
            label=TRANSLATIONS[st.session_state["lang"]]["sidebar_lang_label"],
            options=list(LANGUAGE_OPTIONS.keys()),
            index=list(LANGUAGE_OPTIONS.keys()).index(st.session_state["lang"]),
            format_func=lambda code: LANGUAGE_OPTIONS[code],
            key="language_selector",
        )
        if selected_lang != st.session_state["lang"]:
            st.session_state["lang"] = selected_lang
            st.rerun()

    lang = st.session_state["lang"]
    t = TRANSLATIONS[lang]
    inject_luxury_css(lang)

    with st.sidebar:
        st.divider()
        st.markdown(f"#### {t['sidebar_hotel_info']}")
        st.markdown(f"**{t['sidebar_phone']}:** <bdi>{html.escape(str(config.get('phone', '')))}</bdi>", unsafe_allow_html=True)
        st.markdown(f"**{t['sidebar_email']}:** <bdi>{html.escape(str(config.get('email', '')))}</bdi>", unsafe_allow_html=True)
        st.markdown(
            f"**{t['sidebar_checkin']}:** <bdi>{html.escape(str(config.get('check_in_time', '15:00')))}</bdi>"
            f" · **{t['sidebar_checkout']}:** <bdi>{html.escape(str(config.get('check_out_time', '12:00')))}</bdi>",
            unsafe_allow_html=True,
        )

        st.divider()
        st.markdown(f"#### {t['sidebar_ai_section']}")
        api_override = st.text_input(
            t["sidebar_api_key_label"],
            type="password",
            help=t["sidebar_api_key_help"],
            key="sidebar_gemini_api_key",
        )
        resolved_api_key = resolve_gemini_api_key(api_override)
        if resolved_api_key:
            st.success(t["sidebar_api_ready"])
        else:
            st.info(t["sidebar_api_missing"])
        st.caption(
            f"{t['sidebar_model_label']}: {config.get('gemini_model', GEMINI_MODEL)}"
        )

    render_hero_banner(config, lang)

    tab_overview, tab_booking, tab_ai, tab_admin = st.tabs(t["tabs"])

    with tab_overview:
        render_overview_tab(config, lang)

    with tab_booking:
        render_booking_tab(config, lang)

    with tab_ai:
        render_ai_concierge_tab(config, lang, resolved_api_key)

    with tab_admin:
        render_admin_tab(config, lang)


if __name__ == "__main__":
    main()
