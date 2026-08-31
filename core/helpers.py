"""Shared HTTP, escaping and UniProt parsing helpers."""
from __future__ import annotations
import os
from typing import Any, Optional
import requests
import streamlit as st

def get_secret(name: str) -> str:
    try:
        value=st.secrets.get(name,"")
        if value: return str(value)
    except Exception: pass
    return os.environ.get(name,"")

def safe_get(url: str, **kwargs) -> Optional[requests.Response]:
    headers=kwargs.pop("headers",{})
    headers.setdefault("User-Agent","ProteinExplorer/3.0 educational Streamlit app")
    try:
        response=requests.get(url,headers=headers,timeout=25,**kwargs)
        response.raise_for_status(); return response
    except requests.RequestException: return None

def esc(text: Any) -> str:
    text=str(text if text is not None else "")
    return text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def location_text(comment: dict) -> str:
    locations=[]
    for item in comment.get("subcellularLocations",[]):
        loc=item.get("location",{}).get("value")
        if loc: locations.append(loc)
    return ", ".join(dict.fromkeys(locations)) or "Not specified"

def comment_text(record: dict, comment_type: str, default: str="Not available.") -> str:
    for comment in record.get("comments",[]):
        if comment.get("commentType")==comment_type:
            values=[x.get("value","") for x in comment.get("texts",[]) if x.get("value")]
            if values: return " ".join(values)
    return default

def _position_value(obj: Any) -> Optional[int]:
    if obj is None: return None
    if isinstance(obj,(int,float,str)):
        try: return int(obj)
        except (TypeError,ValueError): return None
    if isinstance(obj,dict):
        value=obj.get("value",obj.get("position"))
        try: return int(value) if value is not None else None
        except (TypeError,ValueError): return None
    return None

def feature_position(feature: dict) -> tuple[Optional[int],Optional[int]]:
    loc=feature.get("location") or {}
    start=_position_value(loc.get("start")); end=_position_value(loc.get("end"))
    if start is None: start=_position_value(loc.get("position"))
    if end is None: end=_position_value(loc.get("position"))
    return start,end

def feature_description(feature: dict) -> str:
    desc=feature.get("description") or feature.get("note") or ""
    if isinstance(desc,dict): desc=desc.get("value","")
    if isinstance(desc,list):
        vals=[]
        for item in desc:
            if isinstance(item,dict): item=item.get("value","")
            if item: vals.append(str(item))
        return "; ".join(vals)
    return str(desc)
