from models.base import Basevn
from libs.wework import get_projects_details

ProjectDetails: Basevn = {
    "name": "Wework_ProjectDetails",
    "get": get_projects_details,
    "transform": lambda rows: rows,
    "schema": [{}],
}
