import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os
import base64

# Configure Streamlit for Azure deployment
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_SERVER_PORT'] = str(os.environ.get('PORT', '8000'))
os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

# Load environment variables from .env file for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, will rely on system environment variables
    pass

st.set_page_config(
    page_title="CyberRX Insurability Audit",
    page_icon="🛡️",
    layout="wide"
)

# 6-digit NAICS Codes Dictionary - Comprehensive industry codes
NAICS_CODES = {
    "111110 - Soybean Farming": "111110",
    "111120 - Oilseed (except Soybean) Farming": "111120",
    "111130 - Dry Pea and Bean Farming": "111130",
    "111140 - Wheat Farming": "111140",
    "111150 - Corn Farming": "111150",
    "111160 - Rice Farming": "111160",
    "111191 - Oilseed and Grain Combination Farming": "111191",
    "111199 - All Other Grain Farming": "111199",
    "111211 - Potato Farming": "111211",
    "111219 - Other Vegetable (except Potato) and Melon Farming": "111219",
    "111310 - Orange Groves": "111310",
    "111320 - Citrus (except Orange) Groves": "111320",
    "111331 - Apple Orchards": "111331",
    "111332 - Grape Vineyards": "111332",
    "111333 - Strawberry Farming": "111333",
    "111334 - Berry (except Strawberry) Farming": "111334",
    "111335 - Tree Nut Farming": "111335",
    "111336 - Fruit and Tree Nut Combination Farming": "111336",
    "111339 - Other Noncitrus Fruit Farming": "111339",
    "111411 - Mushroom Production": "111411",
    "111419 - Other Food Crops Grown Under Cover": "111419",
    "111421 - Nursery and Tree Production": "111421",
    "111422 - Floriculture Production": "111422",
    "111910 - Tobacco Farming": "111910",
    "111920 - Cotton Farming": "111920",
    "111930 - Sugarcane Farming": "111930",
    "111940 - Hay Farming": "111940",
    "111991 - Sugar Beet Farming": "111991",
    "111992 - Peanut Farming": "111992",
    "111998 - All Other Miscellaneous Crop Farming": "111998",
    "112111 - Beef Cattle Ranching and Farming": "112111",
    "112112 - Cattle Feedlots": "112112",
    "112120 - Dairy Cattle and Milk Production": "112120",
    "112130 - Dual-Purpose Cattle Ranching and Farming": "112130",
    "112210 - Hog and Pig Farming": "112210",
    "112310 - Chicken Egg Production": "112310",
    "112320 - Broilers and Other Meat Type Chicken Production": "112320",
    "112330 - Turkey Production": "112330",
    "112340 - Poultry Hatcheries": "112340",
    "112390 - Other Poultry Production": "112390",
    "112410 - Sheep Farming": "112410",
    "112420 - Goat Farming": "112420",
    "112511 - Finfish Farming and Fish Hatcheries": "112511",
    "112512 - Shellfish Farming": "112512",
    "112519 - Other Aquaculture": "112519",
    "112910 - Apiculture": "112910",
    "112920 - Horse and Other Equine Production": "112920",
    "112930 - Fur-Bearing Animal and Rabbit Production": "112930",
    "112990 - All Other Animal Production": "112990",
    "221110 - Electric Power Generation": "221110",
    "221121 - Electric Bulk Power Transmission and Control": "221121",
    "221122 - Electric Power Distribution": "221122",
    "221210 - Natural Gas Distribution": "221210",
    "221310 - Water Supply and Irrigation Systems": "221310",
    "221320 - Sewage Treatment Facilities": "221320",
    "221330 - Steam and Air-Conditioning Supply": "221330",
    "236115 - New Single-Family Housing Construction": "236115",
    "236116 - New Multifamily Housing Construction": "236116",
    "236117 - New Housing Operative Builders": "236117",
    "236118 - Residential Remodelers": "236118",
    "236210 - Industrial Building Construction": "236210",
    "236220 - Commercial and Institutional Building Construction": "236220",
    "237110 - Water and Sewer Line and Related Structures Construction": "237110",
    "237120 - Oil and Gas Pipeline and Related Structures Construction": "237120",
    "237130 - Power and Communication Line and Related Structures Construction": "237130",
    "237210 - Land Subdivision": "237210",
    "237310 - Highway, Street, and Bridge Construction": "237310",
    "237990 - Other Heavy and Civil Engineering Construction": "237990",
    "238110 - Poured Concrete Foundation and Structure Contractors": "238110",
    "238120 - Structural Steel and Precast Concrete Contractors": "238120",
    "238130 - Framing Contractors": "238130",
    "238140 - Masonry Contractors": "238140",
    "238150 - Glass and Glazing Contractors": "238150",
    "238160 - Roofing Contractors": "238160",
    "238170 - Siding Contractors": "238170",
    "238190 - Other Foundation, Structure, and Building Exterior Contractors": "238190",
    "238210 - Electrical Contractors and Other Wiring Installation Contractors": "238210",
    "238220 - Plumbing, Heating, and Air-Conditioning Contractors": "238220",
    "238290 - Other Building Equipment Contractors": "238290",
    "238310 - Drywall and Insulation Contractors": "238310",
    "238320 - Painting and Wall Covering Contractors": "238320",
    "238330 - Flooring Contractors": "238330",
    "238340 - Tile and Terrazzo Contractors": "238340",
    "238350 - Finish Carpentry Contractors": "238350",
    "238390 - Other Building Finishing Contractors": "238390",
    "238910 - Site Preparation Contractors": "238910",
    "238990 - All Other Specialty Trade Contractors": "238990",
    "311111 - Dog and Cat Food Manufacturing": "311111",
    "311119 - Other Animal Food Manufacturing": "311119",
    "311211 - Flour Milling": "311211",
    "311212 - Rice Milling": "311212",
    "311213 - Malt Manufacturing": "311213",
    "311221 - Wet Corn Milling": "311221",
    "311222 - Soybean Processing": "311222",
    "311223 - Other Oilseed Processing": "311223",
    "311225 - Fats and Oils Refining and Blending": "311225",
    "311230 - Breakfast Cereal Manufacturing": "311230",
    "311311 - Sugarcane Mills": "311311",
    "311312 - Cane Sugar Refining": "311312",
    "311313 - Beet Sugar Manufacturing": "311313",
    "311320 - Chocolate and Confectionery Manufacturing from Cacao Beans": "311320",
    "311330 - Confectionery Manufacturing from Purchased Chocolate": "311330",
    "311340 - Nonchocolate Confectionery Manufacturing": "311340",
    "311351 - Chocolate and Confectionery Manufacturing from Cacao Beans": "311351",
    "311352 - Confectionery Manufacturing from Purchased Chocolate": "311352",
    "311411 - Frozen Fruit, Juice, and Vegetable Manufacturing": "311411",
    "311412 - Frozen Specialty Food Manufacturing": "311412",
    "311421 - Fruit and Vegetable Canning": "311421",
    "311422 - Specialty Canning": "311422",
    "311423 - Dried and Dehydrated Food Manufacturing": "311423",
    "311511 - Fluid Milk Manufacturing": "311511",
    "311512 - Creamery Butter Manufacturing": "311512",
    "311513 - Cheese Manufacturing": "311513",
    "311514 - Dry, Condensed, and Evaporated Dairy Product Manufacturing": "311514",
    "311520 - Ice Cream and Frozen Dessert Manufacturing": "311520",
    "311611 - Animal (except Poultry) Slaughtering": "311611",
    "311612 - Meat Processed from Carcasses": "311612",
    "311613 - Rendering and Meat Byproduct Processing": "311613",
    "311615 - Poultry Processing": "311615",
    "311711 - Seafood Canning": "311711",
    "311712 - Fresh and Frozen Seafood Processing": "311712",
    "311813 - Frozen Cakes, Pies, and Other Pastries Manufacturing": "311813",
    "311821 - Cookie and Cracker Manufacturing": "311821",
    "311822 - Flour Mixes and Dough Manufacturing from Purchased Flour": "311822",
    "311823 - Dry Pasta Manufacturing": "311823",
    "311830 - Tortilla Manufacturing": "311830",
    "311911 - Roasted Nuts and Peanut Butter Manufacturing": "311911",
    "311919 - Other Snack Food Manufacturing": "311919",
    "311920 - Coffee and Tea Manufacturing": "311920",
    "311930 - Flavoring Syrup and Concentrate Manufacturing": "311930",
    "311941 - Mayonnaise, Dressing, and Other Prepared Sauce Manufacturing": "311941",
    "311942 - Spice and Extract Manufacturing": "311942",
    "311991 - Perishable Prepared Food Manufacturing": "311991",
    "311999 - All Other Miscellaneous Food Manufacturing": "311999",
    "312111 - Soft Drink Manufacturing": "312111",
    "312112 - Bottled Water Manufacturing": "312112",
    "312113 - Ice Manufacturing": "312113",
    "312120 - Breweries": "312120",
    "312130 - Wineries": "312130",
    "312140 - Distilleries": "312140",
    "312210 - Tobacco Stemming and Redrying": "312210",
    "312221 - Cigarette Manufacturing": "312221",
    "312229 - Other Tobacco Product Manufacturing": "312229",
    "423110 - Automobile and Other Motor Vehicle Merchant Wholesalers": "423110",
    "423120 - Motor Vehicle Supplies and New Parts Merchant Wholesalers": "423120",
    "423130 - Tire and Tube Merchant Wholesalers": "423130",
    "423140 - Motor Vehicle Parts (Used) Merchant Wholesalers": "423140",
    "423210 - Furniture Merchant Wholesalers": "423210",
    "423220 - Home Furnishing Merchant Wholesalers": "423220",
    "423310 - Lumber, Plywood, Millwork, and Wood Panel Merchant Wholesalers": "423310",
    "423320 - Brick, Stone, and Related Construction Material Merchant Wholesalers": "423320",
    "423330 - Roofing, Siding, and Insulation Material Merchant Wholesalers": "423330",
    "423390 - Other Construction Material Merchant Wholesalers": "423390",
    "423410 - Photographic Equipment and Supplies Merchant Wholesalers": "423410",
    "423420 - Office Equipment Merchant Wholesalers": "423420",
    "423430 - Computer and Computer Peripheral Equipment and Software Merchant Wholesalers": "423430",
    "423440 - Other Commercial Equipment Merchant Wholesalers": "423440",
    "423450 - Medical, Dental, and Hospital Equipment and Supplies Merchant Wholesalers": "423450",
    "423460 - Ophthalmic Goods Merchant Wholesalers": "423460",
    "423490 - Other Professional Equipment and Supplies Merchant Wholesalers": "423490",
    "423510 - Metal Service Centers and Other Metal Merchant Wholesalers": "423510",
    "423520 - Coal and Other Mineral and Ore Merchant Wholesalers": "423520",
    "423610 - Electrical Apparatus and Equipment, Wiring Supplies, and Related Equipment Merchant Wholesalers": "423610",
    "423620 - Electrical and Electronic Appliance, Television, and Radio Set Merchant Wholesalers": "423620",
    "423690 - Other Electronic Parts and Equipment Merchant Wholesalers": "423690",
    "423710 - Hardware Merchant Wholesalers": "423710",
    "423720 - Plumbing and Heating Equipment and Supplies (Hydronics) Merchant Wholesalers": "423720",
    "423730 - Warm Air Heating and Air-Conditioning Equipment and Supplies Merchant Wholesalers": "423730",
    "423740 - Refrigeration Equipment and Supplies Merchant Wholesalers": "423740",
    "423810 - Construction and Mining (except Oil Well) Machinery and Equipment Merchant Wholesalers": "423810",
    "423820 - Farm and Garden Machinery and Equipment Merchant Wholesalers": "423820",
    "423830 - Industrial Machinery and Equipment Merchant Wholesalers": "423830",
    "423840 - Industrial Supplies Merchant Wholesalers": "423840",
    "423850 - Service Establishment Equipment and Supplies Merchant Wholesalers": "423850",
    "423860 - Transportation Equipment and Supplies (except Motor Vehicle) Merchant Wholesalers": "423860",
    "423910 - Sporting and Recreational Goods and Supplies Merchant Wholesalers": "423910",
    "423920 - Toy and Hobby Goods and Supplies Merchant Wholesalers": "423920",
    "423930 - Recyclable Material Merchant Wholesalers": "423930",
    "423940 - Jewelry, Watch, Precious Stone, and Precious Metal Merchant Wholesalers": "423940",
    "423990 - Other Miscellaneous Durable Goods Merchant Wholesalers": "423990",
    "441110 - New Car Dealers": "441110",
    "441120 - Used Car Dealers": "441120",
    "441210 - Recreational Vehicle Dealers": "441210",
    "441222 - Boat Dealers": "441222",
    "441228 - Motorcycle, ATV, and All Other Motor Vehicle Dealers": "441228",
    "441310 - Automotive Parts and Accessories Stores": "441310",
    "441320 - Tire Dealers": "441320",
    "442110 - Furniture Stores": "442110",
    "442210 - Floor Covering Stores": "442210",
    "442291 - Window Treatment Stores": "442291",
    "442299 - All Other Home Furnishings Stores": "442299",
    "443142 - Electronics Stores": "443142",
    "443143 - Computer and Software Stores": "443143",
    "443144 - Camera and Photographic Supplies Stores": "443144",
    "444110 - Home Centers": "444110",
    "444120 - Paint and Wallpaper Stores": "444120",
    "444130 - Hardware Stores": "444130",
    "444190 - Other Building Material Dealers": "444190",
    "444220 - Nursery, Garden Center, and Farm Supply Stores": "444220",
    "445110 - Supermarkets and Other Grocery (except Convenience) Stores": "445110",
    "445120 - Convenience Stores": "445120",
    "445210 - Meat Markets": "445210",
    "445220 - Fish and Seafood Markets": "445220",
    "445230 - Fruit and Vegetable Markets": "445230",
    "445291 - Baked Goods Stores": "445291",
    "445292 - Confectionery and Nut Stores": "445292",
    "445299 - All Other Specialty Food Stores": "445299",
    "445310 - Beer, Wine, and Liquor Stores": "445310",
    "446110 - Pharmacies and Drug Stores": "446110",
    "446120 - Cosmetics, Beauty Supplies, and Perfume Stores": "446120",
    "446130 - Optical Goods Stores": "446130",
    "446191 - Food (Health) Supplement Stores": "446191",
    "446199 - All Other Health and Personal Care Stores": "446199",
    "447110 - Gasoline Stations with Convenience Stores": "447110",
    "447190 - Other Gasoline Stations": "447190",
    "448110 - Men's Clothing Stores": "448110",
    "448120 - Women's Clothing Stores": "448120",
    "448130 - Children's and Infants' Clothing Stores": "448130",
    "448140 - Family Clothing Stores": "448140",
    "448150 - Clothing Accessories Stores": "448150",
    "448190 - Other Clothing Stores": "448190",
    "448210 - Shoe Stores": "448210",
    "448310 - Jewelry Stores": "448310",
    "448320 - Luggage and Leather Goods Stores": "448320",
    "451110 - Sporting Goods Stores": "451110",
    "451120 - Hobby, Toy, and Game Stores": "451120",
    "451130 - Sewing, Needlework, and Piece Goods Stores": "451130",
    "451140 - Musical Instrument and Supplies Stores": "451140",
    "451211 - Book Stores": "451211",
    "451212 - News Dealers and Newsstands": "451212",
    "452111 - Department Stores (except Discount Department Stores)": "452111",
    "452112 - Discount Department Stores": "452112",
    "452210 - Warehouse Clubs and Supercenters": "452210",
    "452311 - Warehouse Clubs and Supercenters": "452311",
    "452319 - All Other General Merchandise Stores": "452319",
    "453110 - Florists": "453110",
    "453210 - Office Supplies and Stationery Stores": "453210",
    "453220 - Gift, Novelty, and Souvenir Stores": "453220",
    "453310 - Used Merchandise Stores": "453310",
    "453390 - Other Miscellaneous Store Retailers": "453390",
    "453910 - Pet and Pet Supplies Stores": "453910",
    "453920 - Art Dealers": "453920",
    "453930 - Mobile Home Dealers": "453930",
    "453991 - Tobacco Stores": "453991",
    "453998 - All Other Miscellaneous Store Retailers (except Tobacco Stores)": "453998",
    "454110 - Electronic Shopping and Mail-Order Houses": "454110",
    "454210 - Vending Machine Operators": "454210",
    "454310 - Fuel Dealers": "454310",
    "454390 - Other Direct Selling Establishments": "454390",
    "511110 - Newspaper Publishers": "511110",
    "511120 - Periodical Publishers": "511120",
    "511130 - Book Publishers": "511130",
    "511140 - Directory and Mailing List Publishers": "511140",
    "511191 - Greeting Card Publishers": "511191",
    "511199 - All Other Publishers": "511199",
    "511210 - Software Publishers": "511210",
    "517110 - Wired Telecommunications Carriers": "517110",
    "517210 - Wireless Telecommunications Carriers (except Satellite)": "517210",
    "517311 - Wired Telecommunications Carriers": "517311",
    "517312 - Wireless Telecommunications Carriers (except Satellite)": "517312",
    "517410 - Satellite Telecommunications": "517410",
    "517510 - Cable and Other Subscription Programming": "517510",
    "517910 - Other Telecommunications": "517910",
    "518111 - Internet Service Providers": "518111",
    "518112 - Web Search Portals": "518112",
    "518210 - Data Processing, Hosting, and Related Services": "518210",
    "519110 - News Syndicates": "519110",
    "519120 - Libraries and Archives": "519120",
    "519190 - All Other Information Services": "519190",
    "522110 - Commercial Banking": "522110",
    "522120 - Savings Institutions": "522120",
    "522130 - Credit Unions": "522130",
    "522190 - Other Depository Credit Intermediation": "522190",
    "522210 - Credit Card Issuing": "522210",
    "522220 - Sales Financing": "522220",
    "522291 - Consumer Lending": "522291",
    "522292 - Real Estate Credit": "522292",
    "522293 - International Trade Financing": "522293",
    "522294 - Secondary Market Financing": "522294",
    "522298 - All Other Nondepository Credit Intermediation": "522298",
    "522310 - Mortgage and Nonmortgage Loan Brokers": "522310",
    "522320 - Financial Transactions Processing, Reserve, and Clearinghouse Activities": "522320",
    "522390 - Other Activities Related to Credit Intermediation": "522390",
    "523110 - Investment Banking and Securities Dealing": "523110",
    "523120 - Securities Brokerage": "523120",
    "523130 - Commodity Contracts Dealing": "523130",
    "523140 - Commodity Contracts Brokerage": "523140",
    "523210 - Securities and Commodity Exchanges": "523210",
    "523910 - Miscellaneous Intermediation": "523910",
    "523920 - Portfolio Management": "523920",
    "523930 - Investment Advice": "523930",
    "523991 - Trust, Fiduciary, and Custody Activities": "523991",
    "523999 - Miscellaneous Financial Investment Activities": "523999",
    "524113 - Direct Life Insurance Carriers": "524113",
    "524114 - Direct Health and Medical Insurance Carriers": "524114",
    "524126 - Direct Property and Casualty Insurance Carriers": "524126",
    "524127 - Direct Title Insurance Carriers": "524127",
    "524128 - Other Direct Insurance (except Life, Health, and Medical) Carriers": "524128",
    "524130 - Reinsurance Carriers": "524130",
    "524210 - Insurance Agencies and Brokerages": "524210",
    "524291 - Claims Adjusting": "524291",
    "524292 - Third Party Administration of Insurance and Pension Funds": "524292",
    "524298 - All Other Insurance Related Activities": "524298",
    "531110 - Lessors of Residential Buildings and Dwellings": "531110",
    "531120 - Lessors of Nonresidential Buildings (except Miniwarehouses)": "531120",
    "531130 - Lessors of Miniwarehouses and Self-Storage Units": "531130",
    "531190 - Lessors of Other Real Estate Property": "531190",
    "531210 - Offices of Real Estate Agents and Brokers": "531210",
    "531311 - Residential Property Managers": "531311",
    "531312 - Nonresidential Property Managers": "531312",
    "531320 - Offices of Real Estate Appraisers": "531320",
    "531390 - Other Activities Related to Real Estate": "531390",
    "532111 - Passenger Car Rental": "532111",
    "532112 - Passenger Car Leasing": "532112",
    "532120 - Truck, Utility Trailer, and RV (Recreational Vehicle) Rental and Leasing": "532120",
    "532210 - Consumer Electronics and Appliances Rental": "532210",
    "532220 - Formal Wear and Costume Rental": "532220",
    "532230 - Video Tape and Disc Rental": "532230",
    "532290 - Other Consumer Goods Rental": "532290",
    "532310 - General Rental Centers": "532310",
    "532411 - Commercial Air, Rail, and Water Transportation Equipment Rental and Leasing": "532411",
    "532412 - Construction, Mining, and Forestry Machinery and Equipment Rental and Leasing": "532412",
    "532420 - Office Machinery and Equipment Rental and Leasing": "532420",
    "541110 - Offices of Lawyers": "541110",
    "541191 - Title Abstract and Settlement Offices": "541191",
    "541199 - All Other Legal Services": "541199",
    "541211 - Offices of Certified Public Accountants": "541211",
    "541213 - Tax Preparation Services": "541213",
    "541214 - Payroll Services": "541214",
    "541219 - Other Accounting Services": "541219",
    "541310 - Architectural Services": "541310",
    "541320 - Landscape Architectural Services": "541320",
    "541330 - Engineering Services": "541330",
    "541340 - Drafting Services": "541340",
    "541350 - Building Inspection Services": "541350",
    "541360 - Geophysical Surveying and Mapping Services": "541360",
    "541370 - Surveying and Mapping (except Geophysical) Services": "541370",
    "541380 - Testing Laboratories": "541380",
    "541410 - Interior Design Services": "541410",
    "541420 - Industrial Design Services": "541420",
    "541430 - Graphic Design Services": "541430",
    "541490 - Other Specialized Design Services": "541490",
    "541511 - Custom Computer Programming Services": "541511",
    "541512 - Computer Systems Design Services": "541512",
    "541513 - Computer Facilities Management Services": "541513",
    "541519 - Other Computer Related Services": "541519",
    "541611 - Administrative Management and General Management Consulting Services": "541611",
    "541612 - Human Resources Consulting Services": "541612",
    "541613 - Marketing Consulting Services": "541613",
    "541614 - Process, Physical Distribution, and Logistics Consulting Services": "541614",
    "541618 - Other Management Consulting Services": "541618",
    "541620 - Environmental Consulting Services": "541620",
    "541690 - Other Scientific and Technical Consulting Services": "541690",
    "541711 - Research and Development in Biotechnology": "541711",
    "541712 - Research and Development in the Physical, Engineering, and Life Sciences (except Biotechnology)": "541712",
    "541720 - Research and Development in the Social Sciences and Humanities": "541720",
    "541810 - Advertising Agencies": "541810",
    "541820 - Public Relations Agencies": "541820",
    "541830 - Media Buying Agencies": "541830",
    "541840 - Media Representatives": "541840",
    "541850 - Outdoor Advertising": "541850",
    "541860 - Direct Mail Advertising": "541860",
    "541870 - Advertising Material Distribution Services": "541870",
    "541890 - Other Services Related to Advertising": "541890",
    "541910 - Marketing Research and Public Opinion Polling": "541910",
    "541921 - Photography Studios, Portrait": "541921",
    "541922 - Commercial Photography": "541922",
    "541930 - Translation and Interpretation Services": "541930",
    "541940 - Veterinary Services": "541940",
    "541990 - All Other Professional, Scientific, and Technical Services": "541990",
    "561110 - Office Administrative Services": "561110",
    "561210 - Facilities Support Services": "561210",
    "561310 - Employment Placement Agencies": "561310",
    "561320 - Temporary Help Services": "561320",
    "561330 - Professional Employer Organizations": "561330",
    "561410 - Document Preparation Services": "561410",
    "561421 - Telephone Answering Services": "561421",
    "561422 - Telemarketing Bureaus and Other Contact Centers": "561422",
    "561431 - Private Mail Centers": "561431",
    "561439 - Other Business Service Centers (including Copy Shops)": "561439",
    "561440 - Collection Agencies": "561440",
    "561450 - Credit Bureaus": "561450",
    "561490 - Other Business Support Services": "561490",
    "561510 - Travel Agencies": "561510",
    "561520 - Tour Operators": "561520",
    "561591 - Convention and Visitors Bureaus": "561591",
    "561599 - All Other Travel Arrangement and Reservation Services": "561599",
    "561611 - Investigation Services": "561611",
    "561612 - Security Guards and Patrol Services": "561612",
    "561613 - Armored Car Services": "561613",
    "561621 - Security Systems Services (except Locksmiths)": "561621",
    "561622 - Locksmiths": "561622",
    "561710 - Exterminating and Pest Control Services": "561710",
    "561720 - Janitorial Services": "561720",
    "561730 - Landscaping Services": "561730",
    "561740 - Carpet and Upholstery Cleaning Services": "561740",
    "561790 - Other Services to Buildings and Dwellings": "561790",
    "561910 - Packaging and Labeling Services": "561910",
    "561920 - Convention and Trade Show Organizers": "561920",
    "561990 - All Other Support Services": "561990",
    "611110 - Elementary and Secondary Schools": "611110",
    "611210 - Junior Colleges": "611210",
    "611310 - Colleges, Universities, and Professional Schools": "611310",
    "611410 - Business and Secretarial Schools": "611410",
    "611420 - Computer Training": "611420",
    "611430 - Professional and Management Development Training": "611430",
    "611511 - Cosmetology and Barber Schools": "611511",
    "611512 - Flight Training": "611512",
    "611513 - Apprenticeship Training": "611513",
    "611519 - Other Technical and Trade Schools": "611519",
    "611610 - Fine Arts Schools": "611610",
    "611620 - Sports and Recreation Instruction": "611620",
    "611630 - Language Schools": "611630",
    "611691 - Exam Preparation and Tutoring": "611691",
    "611692 - Automobile Driving Schools": "611692",
    "611699 - All Other Miscellaneous Schools and Instruction": "611699",
    "611710 - Educational Support Services": "611710",
    "621111 - Offices of Physicians (except Mental Health Specialists)": "621111",
    "621112 - Offices of Physicians, Mental Health Specialists": "621112",
    "621210 - Offices of Dentists": "621210",
    "621310 - Offices of Chiropractors": "621310",
    "621320 - Offices of Optometrists": "621320",
    "621330 - Offices of Mental Health Practitioners (except Physicians)": "621330",
    "621340 - Offices of Physical, Occupational and Speech Therapists, and Audiologists": "621340",
    "621391 - Offices of Podiatrists": "621391",
    "621399 - Offices of All Other Miscellaneous Health Practitioners": "621399",
    "621410 - Family Planning Centers": "621410",
    "621420 - Outpatient Mental Health and Substance Abuse Centers": "621420",
    "621491 - HMO Medical Centers": "621491",
    "621492 - Kidney Dialysis Centers": "621492",
    "621493 - Freestanding Ambulatory Surgical and Emergency Centers": "621493",
    "621498 - All Other Outpatient Care Centers": "621498",
    "621511 - Medical Laboratories": "621511",
    "621512 - Diagnostic Imaging Centers": "621512",
    "621610 - Home Health Care Services": "621610",
    "621910 - Ambulance Services": "621910",
    "621991 - Blood and Organ Banks": "621991",
    "621999 - All Other Miscellaneous Ambulatory Health Care Services": "621999",
    "622110 - General Medical and Surgical Hospitals": "622110",
    "622210 - Psychiatric and Substance Abuse Hospitals": "622210",
    "622310 - Specialty (except Psychiatric and Substance Abuse) Hospitals": "622310",
    "623110 - Nursing Care Facilities (Skilled Nursing Facilities)": "623110",
    "623210 - Residential Intellectual and Developmental Disability Facilities": "623210",
    "623220 - Residential Mental Health and Substance Abuse Facilities": "623220",
    "623311 - Continuing Care Retirement Communities": "623311",
    "623312 - Assisted Living Facilities for the Elderly": "623312",
    "623990 - Other Residential Care Facilities": "623990",
    "624110 - Child and Youth Services": "624110",
    "624120 - Services for the Elderly and Persons with Disabilities": "624120",
    "624190 - Other Individual and Family Services": "624190",
    "624210 - Community Food Services": "624210",
    "624221 - Temporary Shelters": "624221",
    "624229 - Other Community Housing Services": "624229",
    "624230 - Emergency and Other Relief Services": "624230",
    "624310 - Vocational Rehabilitation Services": "624310",
    "624410 - Child Day Care Services": "624410",
    "711110 - Theater Companies and Dinner Theaters": "711110",
    "711120 - Dance Companies": "711120",
    "711130 - Musical Groups and Artists": "711130",
    "711190 - Other Performing Arts Companies": "711190",
    "711211 - Sports Teams and Clubs": "711211",
    "711212 - Racetracks": "711212",
    "711219 - Other Spectator Sports": "711219",
    "711310 - Promoters of Performing Arts, Sports, and Similar Events with Facilities": "711310",
    "711320 - Promoters of Performing Arts, Sports, and Similar Events without Facilities": "711320",
    "711410 - Agents and Managers for Artists, Athletes, Entertainers, and Other Public Figures": "711410",
    "711510 - Independent Artists, Writers, and Performers": "711510",
    "712110 - Museums": "712110",
    "712120 - Historical Sites": "712120",
    "712130 - Zoos and Botanical Gardens": "712130",
    "712190 - Nature Parks and Other Similar Institutions": "712190",
    "713110 - Amusement and Theme Parks": "713110",
    "713120 - Amusement Arcades": "713120",
    "713210 - Casinos (except Casino Hotels)": "713210",
    "713290 - Other Gambling Industries": "713290",
    "713910 - Golf Courses and Country Clubs": "713910",
    "713920 - Skiing Facilities": "713920",
    "713930 - Marinas": "713930",
    "713940 - Fitness and Recreational Sports Centers": "713940",
    "713950 - Bowling Centers": "713950",
    "713990 - All Other Amusement and Recreation Industries": "713990",
    "721110 - Hotels (except Casino Hotels) and Motels": "721110",
    "721120 - Casino Hotels": "721120",
    "721191 - Bed and Breakfast Inns": "721191",
    "721199 - All Other Traveler Accommodation": "721199",
    "721214 - Recreational and Vacation Camps (except Campgrounds)": "721214",
    "721211 - RV (Recreational Vehicle) Parks and Campgrounds": "721211",
    "722110 - Full-Service Restaurants": "722110",
    "722211 - Limited-Service Restaurants": "722211",
    "722212 - Cafeterias, Grill Buffets, and Buffets": "722212",
    "722213 - Snack and Nonalcoholic Beverage Bars": "722213",
    "722310 - Food Service Contractors": "722310",
    "722320 - Caterers": "722320",
    "722330 - Mobile Food Services": "722330",
    "722410 - Drinking Places (Alcoholic Beverages)": "722410",
    "811111 - General Automotive Repair": "811111",
    "811112 - Automotive Exhaust System Repair": "811112",
    "811113 - Automotive Transmission Repair": "811113",
    "811118 - Other Automotive Mechanical and Electrical Repair and Maintenance": "811118",
    "811121 - Automotive Body, Paint, and Upholstery Repair and Maintenance": "811121",
    "811122 - Automotive Glass Replacement Shops": "811122",
    "811191 - Automotive Oil Change and Lubrication Shops": "811191",
    "811192 - Car Washes": "811192",
    "811198 - All Other Automotive Repair and Maintenance": "811198",
    "811211 - Consumer Electronics Repair and Maintenance": "811211",
    "811212 - Computer and Office Machine Repair and Maintenance": "811212",
    "811213 - Communication Equipment Repair and Maintenance": "811213",
    "811219 - Other Electronic and Precision Equipment Repair and Maintenance": "811219",
    "811310 - Commercial and Industrial Machinery and Equipment (except Automotive and Electronic) Repair and Maintenance": "811310",
    "811411 - Home and Garden Equipment Repair and Maintenance": "811411",
    "811412 - Appliance Repair and Maintenance": "811412",
    "811420 - Reupholstery and Furniture Repair": "811420",
    "811430 - Footwear and Leather Goods Repair": "811430",
    "811490 - Other Personal and Household Goods Repair and Maintenance": "811490",
    "812111 - Barber Shops": "812111",
    "812112 - Beauty Salons": "812112",
    "812113 - Nail Salons": "812113",
    "812191 - Diet and Weight Reducing Centers": "812191",
    "812199 - Other Personal Care Services": "812199",
    "812210 - Funeral Homes and Funeral Services": "812210",
    "812220 - Cemeteries and Crematories": "812220",
    "812310 - Coin-Operated Laundries and Drycleaners": "812310",
    "812320 - Drycleaning and Laundry Services (except Coin-Operated)": "812320",
    "812331 - Linen Supply": "812331",
    "812332 - Industrial Launderers": "812332",
    "812910 - Pet Care (except Veterinary) Services": "812910",
    "812921 - Photofinishing Laboratories (except One-Hour)": "812921",
    "812922 - One-Hour Photofinishing": "812922",
    "812930 - Parking Lots and Garages": "812930",
    "812990 - All Other Personal Services": "812990",
    "813110 - Religious Organizations": "813110",
    "813211 - Grantmaking Foundations": "813211",
    "813212 - Voluntary Health Organizations": "813212",
    "813219 - Other Grantmaking and Giving Services": "813219",
    "813311 - Human Rights Organizations": "813311",
    "813312 - Environment, Conservation and Wildlife Organizations": "813312",
    "813319 - Other Social Advocacy Organizations": "813319",
    "813410 - Civic and Social Organizations": "813410",
    "813910 - Business Associations": "813910",
    "813920 - Professional Organizations": "813920",
    "813930 - Labor Unions and Similar Labor Organizations": "813930",
    "813940 - Political Organizations": "813940",
    "813990 - Other Similar Organizations (except Business, Professional, Labor, and Political Organizations)": "813990"
}

def send_assessment_email(csv_data, filename, assessment_type, form_data, is_msp_only=False):
    """Send assessment CSV via SendGrid email"""
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail, Attachment
        
        sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
        if not sendgrid_api_key:
            st.error("❌ Email service not configured. SENDGRID_API_KEY environment variable not set.")
            return False
        
        sg = SendGridAPIClient(api_key=sendgrid_api_key)
        
        if is_msp_only:
            subject = f"MSP Security Assessment - {form_data.get('organization_name', 'Unknown Client')} - {form_data.get('msp_name', 'Unknown MSP')}"
        else:
            subject = f"MSP Client Audit - {assessment_type} - {form_data.get('organization_name', 'Unknown Client')}"
        
        # Add cyber insurance info to email
        cyber_insurance_info = ""
        if form_data.get('has_cyber_insurance') == 'Yes':
            cyber_insurance_info = f"""
            <p><strong>Cyber Insurance:</strong> Yes (Effective: {form_data.get('cyber_insurance_effective_date', 'N/A')})</p>
            <p><strong>⚠️ ACTION REQUIRED:</strong> Please send a copy of the client's cyber insurance policy to support@seedpodcyber.com</p>
            """
        elif not is_msp_only:
            cyber_insurance_info = "<p><strong>Cyber Insurance:</strong> No</p>"
        
        if is_msp_only:
            html_content = f"""
            <h2>MSP Security Assessment Submission</h2>
            <p><strong>Assessment Type:</strong> Security Questions Only (Client portion pending)</p>
            <p><strong>Organization:</strong> {form_data.get('organization_name', 'N/A')}</p>
            <p><strong>MSP:</strong> {form_data.get('msp_name', 'N/A')}</p>
            <p><strong>MSP Contact:</strong> {form_data.get('first_name', '')} {form_data.get('last_name', '')}</p>
            <p><strong>MSP Email:</strong> {form_data.get('email', 'N/A')}</p>
            <p><strong>Submission Date:</strong> {form_data.get('submission_date', 'N/A')}</p>
            
            <p><strong>Status:</strong> An email has been sent to the client to complete the business information portion of the audit.</p>
            
            <p>Please find the MSP security assessment data attached as a CSV file.</p>
            
            <hr>
            <p><em>This security assessment was submitted through the MSP Client Insurability Assessment platform.</em></p>
            """
        else:
            html_content = f"""
            <h2>New CyberRX Insurability Audit Submission</h2>
            <p><strong>Assessment Type:</strong> {assessment_type}</p>
            <p><strong>Organization:</strong> {form_data.get('organization_name', 'N/A')}</p>
            <p><strong>Contact:</strong> {form_data.get('first_name', '')} {form_data.get('last_name', '')}</p>
            <p><strong>Email:</strong> {form_data.get('email', 'N/A')}</p>
            <p><strong>MSP:</strong> {form_data.get('msp_name', 'N/A')}</p>
            <p><strong>Submission Date:</strong> {form_data.get('submission_date', 'N/A')}</p>
            {cyber_insurance_info}
            
            <p>Please find the detailed client audit data attached as a CSV file.</p>
            
            <hr>
            <p><em>This audit was submitted through the MSP Client Insurability Assessment platform.</em></p>
            """
        
        message = Mail(
            from_email='noreply@seedpodcyber.com',
            to_emails='support@seedpodcyber.com',
            subject=subject,
            html_content=html_content
        )
        
        encoded_csv = base64.b64encode(csv_data.encode()).decode()
        attachment = Attachment(
            file_content=encoded_csv,
            file_type="text/csv",
            file_name=filename,
            disposition="attachment"
        )
        message.attachment = attachment
        
        response = sg.send(message)
        return response.status_code == 202
        
    except ImportError:
        st.error("❌ SendGrid not installed. Please run: pip install sendgrid")
        return False
    except Exception as e:
        st.error(f"❌ Email sending failed: {str(e)}")
        return False

def send_client_follow_up_email(client_email, client_name, organization_name, msp_name, msp_contact_name):
    """Send follow-up email to client to complete the business information"""
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
        if not sendgrid_api_key:
            return False
        
        sg = SendGridAPIClient(api_key=sendgrid_api_key)
        
        # Generate a unique client completion URL (in production, this would be a proper URL)
        client_completion_url = f"https://mspclientbiz-hnhadbc8dhc7a6bs.centralus-01.azurewebsites.net"
        
        subject = f"Complete Your Client Information - Cyber Insurance Audit for {organization_name}"
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #009D4F; color: white; padding: 2rem; text-align: center;">
                <h1>SeedPod Cyber</h1>
                <h2>Client Information Required</h2>
            </div>
            
            <div style="padding: 2rem; background: #f8f9fa;">
                <p>Dear {client_name},</p>
                
                <p>Your MSP partner <strong>{msp_name}</strong> (represented by {msp_contact_name}) has completed the security assessment portion of your cyber insurance audit. To complete the process, we need some additional business information from you.</p>
                
                <p>The password for this assessment is - SeedPod2025Client! </p>

                <h3>What you need to complete:</h3>
                <ul>
                    <li>✅ Basic organization information</li>
                    <li>✅ Loss history questions</li>
                    <li>✅ Authentication procedures</li>
                    <li>✅ Cyber insurance policy details (if applicable)</li>
                </ul>
                
                <div style="text-align: center; margin: 2rem 0;">
                    <a href="{client_completion_url}" style="background: #009D4F; color: white; padding: 1rem 2rem; text-decoration: none; border-radius: 8px; font-weight: bold;">Complete Client Information</a>
                </div>
                
                <h3>Important:</h3>
                <p>If your organization has cyber insurance, please have your policy document ready to send to <a href="mailto:support@seedpodcyber.com">support@seedpodcyber.com</a> as part of this audit process.</p>
                
                <p>If you have any questions about this audit or need assistance, please contact:</p>
                <ul>
                    <li><strong>Your MSP:</strong> {msp_name} ({msp_contact_name})</li>
                    <li><strong>SeedPod Cyber Support:</strong> <a href="mailto:support@seedpodcyber.com">support@seedpodcyber.com</a></li>
                </ul>
                
                <p>Thank you for your cooperation with this important security audit.</p>
                
                <p>Best regards,<br>
                The SeedPod Cyber Team</p>
            </div>
            
            <div style="background: #353535; color: white; padding: 1rem; text-align: center; font-size: 0.9em;">
                Copyright 2025 SeedPod Cyber LLC, All Rights Reserved
            </div>
        </div>
        """
        
        message = Mail(
            from_email='noreply@seedpodcyber.com',
            to_emails=client_email,
            subject=subject,
            html_content=html_content
        )
        
        # CC the MSP contact
        message.add_cc(st.session_state.get('msp_email', ''))
        
        response = sg.send(message)
        return response.status_code == 202
        
    except Exception as e:
        st.error(f"❌ Client follow-up email failed: {str(e)}")
        return False

def create_tooltip(question_text, tooltip_text):
    """Create a question with tooltip functionality"""
    return f"""
    <div class="question-with-tooltip">
        <span class="question-text">{question_text}</span>
        <div class="tooltip">ℹ️
            <span class="tooltiptext">{tooltip_text}</span>
        </div>
    </div>
    """

def format_currency(amount):
    """Format number as currency with commas and no decimals"""
    if amount == 0:
        return "$0"
    return f"${amount:,.0f}"

def display_currency_input(label, key, help_text="", tooltip_text=""):
    """Display currency input with live formatting"""
    if tooltip_text:
        st.markdown(create_tooltip(label, tooltip_text), unsafe_allow_html=True)
    else:
        st.markdown(f"**{label}**")
    
    # Input with proper formatting
    value = st.number_input(
        f"Amount in USD",
        min_value=0,
        key=key,
        step=1000,
        value=0,
        help=help_text,
        label_visibility="collapsed"
    )
    
    # Display formatted currency immediately below input
    if value > 0:
        st.markdown(f"<div style='color: #009D4F; font-weight: bold; font-size: 1.1em; margin-top: -10px; margin-bottom: 15px;'>💰 {format_currency(value)}</div>", unsafe_allow_html=True)
    
    return value

# Access Control System
def check_access():
    """Check if user has entered valid access key"""
    if 'access_granted' not in st.session_state:
        st.session_state.access_granted = False
    
    if not st.session_state.access_granted:
        # SeedPod Logo for login page
        try:
            st.markdown('<div style="text-align: center; margin: 2rem 0;">', unsafe_allow_html=True)
            st.image('seedpod_logo.png', width=400)
            st.markdown('</div>', unsafe_allow_html=True)
        except:
            st.markdown("""
            <div style="text-align: center; margin: 2rem 0;">
                <div style="display: inline-block; padding: 1rem 2rem; border: 3px solid #009D4F; border-radius: 10px;">
                    <h1 style="color: #009D4F; font-size: 2.5rem; font-weight: 800; margin: 0;">SeedPod</h1>
                    <h2 style="color: #013220; font-size: 1.5rem; font-weight: 600; margin: 0;">CYBER</h2>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Access key login form
        st.markdown("""
        <div style="max-width: 500px; margin: 2rem auto; padding: 2rem; border: 2px solid #009D4F; border-radius: 10px; background: #F8F9FA;">
            <h2 style="color: #013220; text-align: center; margin-bottom: 1rem;">🛡️ Client Audit Access Required</h2>
            <p style="text-align: center; color: #666; margin-bottom: 2rem;">
                Please enter your access key to continue to the CyberRX Insurability Audit.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Access key input
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            access_key = st.text_input(
                "Access Key:",
                type="password",
                placeholder="Enter your access key",
                help="Contact support@seedpodcyber.com if you need an access key"
            )
            
            if st.button("🚀 Access Client Audit", use_container_width=True, type="primary"):
                # Check access key against environment variable
                valid_key = os.getenv('CLIENT_ACCESS_KEY', 'seedpod2025client')  # Default for testing
                
                if access_key == valid_key:
                    st.session_state.access_granted = True
                    st.success("✅ Access granted! Redirecting...")
                    st.rerun()
                elif access_key:
                    st.error("❌ Invalid access key. Please check your key and try again.")
                    st.info("💡 Contact support@seedpodcyber.com if you need assistance.")
                else:
                    st.warning("⚠️ Please enter an access key.")
        
        # Contact information
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9em;">
            <p><strong>Need an access key?</strong></p>
            <p>Contact: <a href="mailto:support@seedpodcyber.com">support@seedpodcyber.com</a></p>
            <p>This client audit tool is available to authorized MSPs and their clients.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Copyright
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 1rem; color: #666; font-size: 0.9em;">
            Copyright 2025 SeedPod Cyber LLC, All Rights Reserved
        </div>
        """, unsafe_allow_html=True)
        
        return False
    
    return True

# Enhanced CSS with SeedPod branding
st.markdown("""
<style>
/* SeedPod Color Palette: #009D4F, #353535, #013220, #E8E9F3, #EAE0CC */

.main-header {
    background: #009D4F;
    color: white;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(0, 157, 79, 0.3);
}

.section-header {
    background: #E8E9F3;
    padding: 1rem;
    border-left: 4px solid #009D4F;
    margin: 1rem 0;
    border-radius: 5px;
    color: #353535;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.section-header h2 {
    color: #013220;
    margin-bottom: 0.5rem;
}

.completion-method {
    background: #EAE0CC;
    padding: 1.5rem;
    border-radius: 10px;
    border: 2px solid #009D4F;
    margin: 2rem 0;
    box-shadow: 0 4px 15px rgba(0, 157, 79, 0.2);
}

.completion-method h2 {
    color: #013220;
    margin-bottom: 1rem;
}

.loss-history {
    background: #E8E9F3;
    padding: 1rem;
    border-radius: 5px;
    border: 2px solid #353535;
    box-shadow: 0 2px 8px rgba(53, 53, 53, 0.2);
}

.loss-history h2 {
    color: #013220;
    margin-bottom: 0.5rem;
}

.security-controls {
    background: #EAE0CC;
    padding: 1rem;
    border-radius: 5px;
    border: 2px solid #009D4F;
    box-shadow: 0 2px 8px rgba(0, 157, 79, 0.2);
}

.security-controls h2 {
    color: #013220;
    margin-bottom: 0.5rem;
}

.cyber-insurance {
    background: #E8F5E8;
    padding: 1rem;
    border-radius: 5px;
    border: 2px solid #009D4F;
    box-shadow: 0 2px 8px rgba(0, 157, 79, 0.2);
}

.cyber-insurance h2 {
    color: #013220;
    margin-bottom: 0.5rem;
}

.question-examples {
    background: rgba(0, 157, 79, 0.1);
    border-left: 3px solid #009D4F;
    padding: 10px 15px;
    margin: 10px 0;
    font-size: 0.9em;
    color: #353535;
    border-radius: 5px;
}

.stButton > button {
    background: #009D4F;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: #013220;
    box-shadow: 0 4px 15px rgba(0, 157, 79, 0.4);
    transform: translateY(-2px);
}

.stFormSubmitButton > button {
    background: #009D4F;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.75rem 2rem;
    font-size: 1.1rem;
}

.stFormSubmitButton > button:hover {
    background: #013220;
    box-shadow: 0 4px 15px rgba(0, 157, 79, 0.4);
}

.stDownloadButton > button {
    background: #009D4F;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 1.1rem;
    padding: 0.75rem;
}

.stDownloadButton > button:hover {
    background: #013220;
    box-shadow: 0 4px 15px rgba(0, 157, 79, 0.4);
}

/* Tooltip Styles */
.tooltip {
    position: relative;
    display: inline-block;
    cursor: help;
    color: #009D4F;
    font-weight: bold;
    margin-left: 5px;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 300px;
    background-color: #353535;
    color: white;
    text-align: left;
    border-radius: 8px;
    padding: 12px;
    position: absolute;
    z-index: 1000;
    bottom: 125%;
    left: 50%;
    margin-left: -150px;
    opacity: 0;
    transition: opacity 0.3s;
    font-size: 0.9em;
    line-height: 1.4;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    border: 1px solid #009D4F;
}

.tooltip .tooltiptext::after {
    content: "";
    position: absolute;
    top: 100%;
    left: 50%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: #353535 transparent transparent transparent;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}

.question-with-tooltip {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.question-text {
    flex-grow: 1;
}
</style>
""", unsafe_allow_html=True)

# Check access before showing any content
if not check_access():
    st.stop()  # Stop execution if access not granted

# Add logout option in sidebar
with st.sidebar:
    st.markdown("---")
    if st.button("🚪 Logout", help="Clear access and return to login"):
        st.session_state.access_granted = False
        st.session_state.clear()  # Clear all session state
        st.rerun()

# SeedPod Logo for main page
try:
    st.markdown('<div style="text-align: center; margin: 2rem 0;">', unsafe_allow_html=True)
    st.image('seedpod_logo.png', width=400)
    st.markdown('</div>', unsafe_allow_html=True)
except:
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <div style="display: inline-block; padding: 1rem 2rem; border: 3px solid #009D4F; border-radius: 10px;">
            <h1 style="color: #009D4F; font-size: 2.5rem; font-weight: 800; margin: 0;">SeedPod</h1>
            <h2 style="color: #013220; font-size: 1.5rem; font-weight: 600; margin: 0;">CYBER</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🛡️ CyberRX Insurability Audit</h1>
    <h3>Cybersecurity Risk Assessment</h3>
    <p>Complete assessment of cyber insurance, security and controls</p>
</div>
""", unsafe_allow_html=True)

# Completion Method Selection
st.markdown("""
<div class="completion-method">
    <h2>📋 Assessment Completion Method</h2>
    <p>Please select how this assessment will be completed:</p>
</div>
""", unsafe_allow_html=True)

if "completion_method" not in st.session_state:
    st.session_state.completion_method = "MSP/Organization completes entire questionnaire"  


completion_method = st.radio(
    "Who will complete this assessment?",
    [
        "MSP/Organization completes entire questionnaire",
        "MSP completes security questions only (organization will complete business information separately)"
    ],
    key="completion_method",
    help="Choose based on your arrangement with the client"
)

# Store completion method in session state

# st.session_state.completion_method = completion_method

# or whatever your default is

# # Now render the widget
# completion_method = st.radio(
#     "Choose a completion method:",
#     ["auto", "manual"],
#     key="completion_method"
# )
is_msp_only = "security questions only" in completion_method

if is_msp_only:
    st.info("""
    🔄 **Split Assessment Process:**
    1. You (MSP) will complete the security-related questions
    2. Upon submission, an email will be sent to your client to complete the business information
    3. Two separate CSV files will be generated for tracking
    """)

with st.form("client_audit_form"):
    # Always show MSP contact information for both modes
    st.markdown('<div class="section-header"><h2>👤 Contact Information</h2><p>Information about the representative completing this assessment</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(create_tooltip(
            "First Name *",
            "Enter the first name of the representative completing this assessment."
        ), unsafe_allow_html=True)
        first_name = st.text_input("Representative First Name", key="first_name", label_visibility="collapsed")
        
        st.markdown(create_tooltip(
            "Last Name *",
            "Enter the last name of the representative completing this assessment."
        ), unsafe_allow_html=True)
        last_name = st.text_input("Representative Last Name", key="last_name", label_visibility="collapsed")
        
        st.markdown(create_tooltip(
            "Email Address *",
            "Enter the email address of the representative for follow-up communications."
        ), unsafe_allow_html=True)
        email = st.text_input("Representative Email", key="email", label_visibility="collapsed")
    
    with col2:
        st.markdown(create_tooltip(
            "Name of Managed Service Provider (or N/A)",
            "Enter the name of the MSP providing services to this organization."
        ), unsafe_allow_html=True)
        msp_name = st.text_input("MSP Company Name", key="msp_name", label_visibility="collapsed")
        
        st.markdown(create_tooltip(
            "Organization Name *",
            "Enter the legal business name of the organization as it appears on official documents."
        ), unsafe_allow_html=True)
        organization_name = st.text_input("Organization Name", key="organization_name", label_visibility="collapsed")
        
        if is_msp_only:
            st.markdown(create_tooltip(
                "Client Contact Name *",
                "Enter the name of the primary client contact who will receive the follow-up email."
            ), unsafe_allow_html=True)
            client_contact_name = st.text_input("Client Contact Name", key="client_contact_name", label_visibility="collapsed")
            
            st.markdown(create_tooltip(
                "Client Email Address *",
                "Enter the email address where the client will receive the follow-up questionnaire."
            ), unsafe_allow_html=True)
            client_email = st.text_input("Client Email", key="client_email", label_visibility="collapsed")

    # Show client information section only if MSP is completing the entire form
    if not is_msp_only:
        st.markdown('<div class="section-header"><h2>🏢 Business Information</h2><p>Basic details about the organization</p></div>', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown(create_tooltip(
                "Organization Address *",
                "Enter the complete address including Street, City, State and Zip Code of the organization."
            ), unsafe_allow_html=True)
            org_address = st.text_area("Organization Address", key="org_address", label_visibility="collapsed")
            
            st.markdown(create_tooltip(
                "Organization Website *",
                "Enter the website URL for the organization (e.g., https://example.com)."
            ), unsafe_allow_html=True)
            org_website = st.text_input("Organization Website", key="org_website", placeholder="https://", label_visibility="collapsed")
            
            st.markdown(create_tooltip(
                "Year of Establishment *",
                "The year the organization was founded or incorporated."
            ), unsafe_allow_html=True)
            year_established = st.number_input("Year of Establishment", min_value=1900, max_value=2025, key="year_established", label_visibility="collapsed")
        
        with col4:
            st.markdown(create_tooltip(
                "NAICS Code *",
                "North American Industry Classification System code that identifies the client's primary business activity. This helps assess industry-specific risks. Search by industry name or enter the 6-digit code."
            ), unsafe_allow_html=True)
            
            # Create searchable NAICS code selectbox
            naics_options = [""] + list(NAICS_CODES.keys())
            selected_naics = st.selectbox(
                "NAICS Code", 
                options=naics_options,
                key="naics_code",
                label_visibility="collapsed",
                help="Start typing to search for your industry"
            )
            
            # Extract just the code from the selection
            if selected_naics:
                naics_code = NAICS_CODES[selected_naics]
            else:
                naics_code = ""
            
            st.markdown(create_tooltip(
                "Total Number of Employees *",
                "Enter the total number of employees in the organization, including full-time and part-time staff."
            ), unsafe_allow_html=True)
            total_employees = st.number_input("Total Employees", min_value=1, key="total_employees", label_visibility="collapsed")
        
        # Revenue Information
        expected_revenue = display_currency_input(
            "Expected Revenue for This Fiscal Year *",
            "expected_revenue",
            "Enter the expected revenue for the current fiscal year rounded to the nearest whole number",
            "Expected total gross revenue for the client's current fiscal year. This helps assess the organization's size and risk profile."
        )
        
        # Cyber Insurance Section
        st.markdown('<div class="cyber-insurance"><h2>🛡️ Cyber Insurance Information</h2><p>Information about the current cyber insurance coverage</p></div>', unsafe_allow_html=True)
        
        col_insurance1, col_insurance2 = st.columns(2)
        
        with col_insurance1:
            st.markdown(create_tooltip(
                "Does your organization currently have cyber insurance? *",
                "Cyber insurance (also called cyber liability insurance) covers financial losses from cyber incidents like data breaches, ransomware attacks, and business interruption due to cyber events."
            ), unsafe_allow_html=True)
            has_cyber_insurance = st.radio("Cyber Insurance Status", ["No", "Yes"], key="has_cyber_insurance", label_visibility="collapsed")
        
        with col_insurance2:
            if has_cyber_insurance == "Yes":
                st.markdown(create_tooltip(
                    "Cyber Insurance Effective Date *",
                    "Enter the date when the current cyber insurance policy became effective (when coverage started)."
                ), unsafe_allow_html=True)
                cyber_insurance_effective_date = st.date_input(
                    "Effective Date", 
                    key="cyber_insurance_effective_date",
                    label_visibility="collapsed",
                    help="Date the cyber insurance policy became effective"
                )
            else:
                cyber_insurance_effective_date = None
        
        # Important instruction for cyber insurance
        if has_cyber_insurance == "Yes":
            st.info("""
            📋 **Important:** Please send a copy of your client's cyber insurance policy to support@seedpodcyber.com 
            for review and verification as part of this audit process.
            """)

        # Loss History Section
        st.markdown('<div class="loss-history"><h2>⚠️ Loss History</h2><p>Please indicate if your organization has suffered from any of these losses in the last 3 years</p></div>', unsafe_allow_html=True)
        
        loss_questions = [
            ("extortion_claim", "Your organization suffered an actual or attempted extortion demand that resulted in a claim"),
            ("data_breach_claim", "Your organization suffered an actual or attempted data breach that resulted in a claim"),
            ("privacy_complaints", "Your organization has experienced a claim or received complaints regarding privacy"),
            ("copyright_infringement", "Your organization performed copyright/trademark infringement that led to a claim"),
            ("cybersecurity_circumstance", "You are aware of a circumstance involving cybersecurity, privacy or copyright/trademark infringement that may give rise to a claim"),
            ("outage_4hours", "Your organization suffered an outage that lasted longer than 4 hours")
        ]
        
        col_loss1, col_loss2 = st.columns(2)
        loss_responses = {}
        
        for i, (key, question) in enumerate(loss_questions):
            with col_loss1 if i % 2 == 0 else col_loss2:
                st.markdown(f"**{question}**")
                loss_responses[key] = st.radio("Response", ["No", "Yes"], key=key, label_visibility="collapsed")
        
        # Authentication Procedures
        st.markdown('<div class="section-header"><h2>🔐 Authentication Procedures</h2></div>', unsafe_allow_html=True)
        
        col_auth1, col_auth2 = st.columns(2)
        
        with col_auth1:
            st.markdown(create_tooltip(
                "Employee Authentication of Customer Information Changes *",
                "Is there a procedure where employees must authenticate all requested changes to customer information (bank accounts, routing numbers, etc.) by calling the vendor?"
            ), unsafe_allow_html=True)
            customer_info_auth = st.radio("Customer Info Authentication", ["No", "Yes"], key="customer_info_auth", label_visibility="collapsed")
        
        with col_auth2:
            st.markdown(create_tooltip(
                "Wire Transfer Request Validation *",
                "Is there a procedure to validate wire transfer requests made by Senior Executives/employees by calling the requestor or face-to-face communication?"
            ), unsafe_allow_html=True)
            wire_transfer_validation = st.radio("Wire Transfer Validation", ["No", "Yes"], key="wire_transfer_validation", label_visibility="collapsed")
    
    # Initialize variables for MSP-only mode
    if is_msp_only:
        org_address = ""
        org_website = ""
        naics_code = ""
        selected_naics = ""
        year_established = 0
        total_employees = 0
        expected_revenue = 0
        has_cyber_insurance = "No"
        cyber_insurance_effective_date = None
        loss_responses = {}
        customer_info_auth = "No"
        wire_transfer_validation = "No"

    # Security Tools Assessment (Always shown)
    st.markdown('<div class="security-controls"><h2>🛠️ Security Tools in Use</h2><p>Please indicate the status of each security tool at the organization</p></div>', unsafe_allow_html=True)
    
    # Create columns for better layout
    col_client1, col_client2 = st.columns(2)
        
    with col_client1:
        st.markdown(create_tooltip(
            "Patch Management (CIS 7.3) *",
            "Automated patch management for operating systems and applications with testing and deployment procedures. Critical for maintaining security baselines and closing vulnerability windows across client environments."
        ), unsafe_allow_html=True)
        client_patch_mgmt = st.radio("Client Patch Management", ["Present", "Not Present", "Partially Present","Not Applicable"], key="client_patch_mgmt", label_visibility="collapsed")
        
        st.markdown(create_tooltip(
            "Multi-Factor Authentication - all remote and local admin (CIS 6.4, 6.5) *",
            "MFA required for all administrative access including remote connections and local admin accounts. Prevents credential-based attacks and unauthorized administrative access to client systems."
        ), unsafe_allow_html=True)
        client_mfa = st.radio("Client MFA for Admin Access", ["Present", "Not Present", "Partially Present","Not Applicable"], key="client_mfa", label_visibility="collapsed")
        
        st.markdown(create_tooltip(
            "Access Control / Strong Password Policy / Unassociated account removal (CIS 5.1, 5.2, 5.3) *",
            "Comprehensive access control including role-based permissions, strong password policies (complexity, length, expiration), and automatic removal of unused accounts. Fundamental for maintaining client system security."
        ), unsafe_allow_html=True)
        client_access_control = st.radio("Client Access Control & Password Policy", ["Present", "Not Present", "Partially Present","Not Applicable"], key="client_access_control", label_visibility="collapsed")
        
        st.markdown(create_tooltip(
            "Secure Remote Access (CIS 13.5) *",
            "VPN or zero-trust remote access solutions with encryption and authentication. Ensures secure connections for remote work and prevents unauthorized network access."
        ), unsafe_allow_html=True)
        client_remote_access = st.radio("Client Secure Remote Access", ["Present", "Not Present", "Partially Present","Not Applicable"], key="client_remote_access", label_visibility="collapsed")
        
        st.markdown(create_tooltip(
            "Next Gen AV / Endpoint Detection and Response (EDR) (CIS 10.1, 13.7) *",
            "Advanced endpoint protection including behavioral analysis, threat hunting, and automated response capabilities. Goes beyond traditional antivirus to detect and respond to sophisticated threats."
        ), unsafe_allow_html=True)
        client_edr = st.radio("Client Next-Gen AV/EDR", ["Present", "Not Present", "Partially Present","Not Applicable"], key="client_edr", label_visibility="collapsed")
        
        st.markdown(create_tooltip(
            "Email Filtering (CIS 9.2, 9.3, 9.4) *",
            "Advanced email security including spam filtering, malware detection, phishing protection, and safe attachment handling. Critical for preventing email-based attacks."
        ), unsafe_allow_html=True)
        client_email_filtering = st.radio("Client Email Filtering", ["Present", "Not Present", "Partially Present","Not Applicable"], key="client_email_filtering", label_visibility="collapsed")
    
    with col_client2:
        st.markdown(create_tooltip(
            "Backup (min 1 online, 1 offline) w/ testing (for on-prem and hybrid environments) (CIS 11.2, 11.4) *",
            "Comprehensive backup strategy with both online (readily accessible) and offline (air-gapped) backups, including regular restore testing to ensure backup integrity and recovery procedures."
        ), unsafe_allow_html=True)
        client_backup = st.radio("Client Backup Strategy", ["Present", "Not Present", "Partially Present","Not Applicable"], key="client_backup", label_visibility="collapsed")
        
        st.markdown(create_tooltip(
            "Encryption on endpoints and in transit (CIS 3.1, 3.11) *",
            "Data encryption for stored data on endpoints (full disk encryption) and data in transit (TLS/SSL for communications). Protects data confidentiality even if devices are lost or communications intercepted."
        ), unsafe_allow_html=True)
        client_encryption = st.radio("Client Encryption (Endpoints & Transit)", ["Present", "Not Present", "Partially Present","Not Applicable"], key="client_encryption", label_visibility="collapsed")
        
        st.markdown(create_tooltip(
            "Security Awareness Training with Phish Simulations (CIS 14.2) *",
            "Regular security awareness training for end users including simulated phishing exercises to test and improve human security behaviors. Critical for preventing social engineering attacks."
        ), unsafe_allow_html=True)
        client_security_training = st.radio("Client Security Awareness Training", ["Present", "Not Present", "Partially Present","Not Applicable"], key="client_security_training", label_visibility="collapsed")
        
        st.markdown(create_tooltip(
            "SPF, DKIM, DMARC (CIS 9.5) *",
            "Email authentication protocols that prevent email spoofing and phishing attacks. SPF verifies sender IP addresses, DKIM validates message authenticity, and DMARC provides policy enforcement."
        ), unsafe_allow_html=True)
        client_email_auth = st.radio("Client SPF/DKIM/DMARC", ["Present", "Not Present", "Partially Present","Not Applicable"], key="client_email_auth", label_visibility="collapsed")
        
        st.markdown(create_tooltip(
            "Remote Desktop Protocol (RDP) and Server Message Block (SMB) ports are blocked (CIS 4.5) *",
            "Network-level blocking of high-risk protocols (RDP port 3389, SMB ports 445/139) from internet access. These protocols are commonly exploited attack vectors and should not be directly accessible from the internet."
        ), unsafe_allow_html=True)
        client_port_blocking = st.radio("Client RDP/SMB Port Blocking", ["Present", "Not Present", "Partially Present","Not Applicable"], key="client_port_blocking", label_visibility="collapsed")
    
    # Additional client security services
    st.markdown("**Managed Security Services:**")
    col_client3, col_client4 = st.columns(2)
    
    with col_client3:
        st.markdown(create_tooltip(
            "Managed Detection and Response (MDR) Services *",
            "24x7 security monitoring and incident response services provided to clients. Includes threat hunting, alert investigation, and incident response coordination."
        ), unsafe_allow_html=True)
        client_mdr = st.radio("Client MDR Services", ["Present", "Not Present", "Partially Present","Not Applicable"], key="client_mdr", label_visibility="collapsed")
    
    with col_client4:
        st.markdown(create_tooltip(
            "Security Operations Center (SOC) Services *",
            "Centralized security monitoring and analysis services including log review, security event correlation, and threat intelligence integration."
        ), unsafe_allow_html=True)
        client_soc = st.radio("Client SOC Services", ["Present", "Not Present", "Partially Present","Not Applicable"], key="client_soc", label_visibility="collapsed")
    
    client_security_comments = st.text_area("Client Security Standards Comments (optional)", 
                                            placeholder="Describe any additional client security requirements, variations by client type, or implementation details",
                                            key="client_security_comments")
    
    # Submit Button
    if is_msp_only:
        submitted = st.form_submit_button("Submit MSP Security Assessment", use_container_width=True)
    else:
        submitted = st.form_submit_button("Submit Complete Audit", use_container_width=True)

# Handle form submission
if submitted:
    # Check required fields based on completion method
    required_fields_validation = []
    
    # Always required fields
    if not first_name or first_name.strip() == "":
        required_fields_validation.append("First Name")
    if not last_name or last_name.strip() == "":
        required_fields_validation.append("Last Name")
    if not email or email.strip() == "":
        required_fields_validation.append("Email Address")
    if not msp_name or msp_name.strip() == "":
        required_fields_validation.append("Name of Managed Service Provider")
    if not organization_name or organization_name.strip() == "":
        required_fields_validation.append("Organization Name")
    
    # Additional required fields for MSP-only mode
    if is_msp_only:
        if not st.session_state.get('client_contact_name', '').strip():
            required_fields_validation.append("Client Contact Name")
        if not st.session_state.get('client_email', '').strip():
            required_fields_validation.append("Client Email Address")
    
    # Additional required fields for complete audit
    if not is_msp_only:
        if not org_address or org_address.strip() == "":
            required_fields_validation.append("Organization Address")
        if not org_website or org_website.strip() == "":
            required_fields_validation.append("Organization Website")
        if not naics_code or naics_code.strip() == "":
            required_fields_validation.append("NAICS Code")
        if not year_established:
            required_fields_validation.append("Year of Establishment")
        if not total_employees:
            required_fields_validation.append("Total Number of Employees")
        if not expected_revenue and expected_revenue != 0:
            required_fields_validation.append("Expected Revenue for This Fiscal Year")
        if has_cyber_insurance == "Yes" and cyber_insurance_effective_date is None:
            required_fields_validation.append("Cyber Insurance Effective Date")
    
    if required_fields_validation:
        st.error(f"❌ Please complete the following required fields: {', '.join(required_fields_validation)}")
    else:
        # Store MSP email for later use
        st.session_state.msp_email = email
        
        # Collect all form data
        form_data = {
            'form_submission_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'submission_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'completion_method': completion_method,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'msp_name': msp_name,
            'organization_name': organization_name,
            'org_address': org_address,
            'org_website': org_website,
            'naics_code': naics_code,
            'naics_description': selected_naics if selected_naics else "",
            'year_established': year_established,
            'total_employees': total_employees,
            'expected_revenue': expected_revenue,
            'has_cyber_insurance': has_cyber_insurance,
            'cyber_insurance_effective_date': cyber_insurance_effective_date.strftime('%Y-%m-%d') if cyber_insurance_effective_date else "",
            'customer_info_auth': customer_info_auth,
            'wire_transfer_validation': wire_transfer_validation,
            'client_patch_mgmt': client_patch_mgmt,
            'client_mfa': client_mfa,
            'client_access_control': client_access_control,
            'client_remote_access': client_remote_access,
            'client_edr': client_edr,
            'client_email_filtering': client_email_filtering,
            'client_backup': client_backup,
            'client_encryption': client_encryption,
            'client_security_training': client_security_training,
            'client_email_auth': client_email_auth,
            'client_port_blocking': client_port_blocking,
            'client_mdr': client_mdr,
            'client_soc': client_soc,
            'client_security_comments': client_security_comments
        }
        
        # Add MSP-only specific fields
        if is_msp_only:
            form_data['client_contact_name'] = st.session_state.get('client_contact_name', '')
            form_data['client_email'] = st.session_state.get('client_email', '')
        
        # Add loss history responses
        form_data.update(loss_responses)
        
        # Store form data in session state
        st.session_state.form_data = form_data
        st.session_state.form_submitted = True
        
        # Create DataFrame and CSV
        df = pd.DataFrame([form_data])
        
        # Generate CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        # Generate filename based on completion method
        if is_msp_only:
            filename = f"msp_security_assessment_{organization_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        else:
            filename = f"client_audit_complete_{organization_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Store CSV data in session state
        st.session_state.csv_data = csv_data
        st.session_state.filename = filename
        
        # Send email with CSV attachment
        email_sent = send_assessment_email(csv_data, filename, "Client Insurability Audit", form_data, is_msp_only)
        
        # Send client follow-up email if MSP-only mode
        client_email_sent = False
        if is_msp_only and email_sent:
            client_email_sent = send_client_follow_up_email(
                st.session_state.get('client_email', ''),
                st.session_state.get('client_contact_name', ''),
                organization_name,
                msp_name,
                f"{first_name} {last_name}"
            )
        
        if email_sent:
            st.session_state.email_sent = True
            st.session_state.client_email_sent = client_email_sent

# Display results after form submission
if st.session_state.get('form_submitted', False):
    # Display success message
    if st.session_state.get('email_sent', False):
        if is_msp_only:
            st.success("✅ MSP Security Assessment submitted successfully!")
            st.info("📧 Your security assessment has been automatically emailed to support@seedpodcyber.com for review.")
            
            if st.session_state.get('client_email_sent', False):
                st.success("📤 Client follow-up email sent successfully!")
                st.info(f"📬 Your client ({st.session_state.get('client_contact_name', 'N/A')}) has been sent an email to complete the business information portion of the audit.")
            else:
                st.warning("⚠️ Client follow-up email failed to send. Please contact your client directly.")
        else:
            st.success("✅ Complete Client audit submitted successfully and sent to our team!")
            st.info("📧 Your client audit has been automatically emailed to support@seedpodcyber.com for review.")
        
        # Additional cyber insurance instruction for complete audits
        if not is_msp_only and st.session_state.form_data.get('has_cyber_insurance') == 'Yes':
            st.warning("🛡️ **Don't forget:** Please send a copy of your client's cyber insurance policy to support@seedpodcyber.com")
    else:
        if is_msp_only:
            st.success("✅ MSP Security Assessment submitted successfully!")
        else:
            st.success("✅ Complete Client audit submitted successfully!")
        st.warning("⚠️ Automatic email delivery failed. Please download your audit and email it manually to support@seedpodcyber.com")
    
    # Download button
    if is_msp_only:
        download_label = "📥 Download MSP Security Assessment (CSV)"
    else:
        download_label = "📥 Download Complete Client Audit Data (CSV)"
    
    st.download_button(
        label=download_label,
        data=st.session_state.csv_data,
        file_name=st.session_state.filename,
        mime="text/csv",
        use_container_width=True
    )
    
    # Display summary
    if is_msp_only:
        summary_title = "📊 Security Assessment Summary"
    else:
        summary_title = "📊 Complete Client Audit Summary"
    
    with st.expander(summary_title, expanded=True):
        col_summary1, col_summary2, col_summary3 = st.columns(3)
        form_data = st.session_state.form_data
        
        with col_summary1:
            st.metric("Organization", form_data['organization_name'])
            st.metric("Contact name", f"{form_data['first_name']} {form_data['last_name']}")
            st.metric("Contact company", form_data['msp_name'])
            
        with col_summary2:
            if not is_msp_only:
                st.metric("Expected Revenue", format_currency(form_data['expected_revenue']))
                st.metric("Employees", f"{form_data['total_employees']:,}")
                st.metric("Year Established", form_data['year_established'])
            else:
                st.metric("Client Contact", form_data.get('client_contact_name', 'N/A'))
                st.metric("Assessment Type", "Security Questions Only")
                st.metric("Status", "Pending Client Completion")
        
        with col_summary3:
            # Count security tools present
            tools_present = sum(1 for k, v in form_data.items() if k.startswith('client_') and v == 'Present')
            st.metric("Security Tools Present", tools_present)
            
            # Count tools partially present
            tools_partial = sum(1 for k, v in form_data.items() if k.startswith('client_') and v == 'Partially Present')
            st.metric("Security Tools Partially Present", tools_partial)
            
            # Cyber insurance status (only for complete audits)
            if not is_msp_only:
                cyber_status = "✅ Yes" if form_data.get('has_cyber_insurance') == 'Yes' else "❌ No"
                st.metric("Cyber Insurance", cyber_status)
            else:
                st.metric("Completion Method", "Split Assessment")
    
    # Instructions for next steps
    if is_msp_only:
        next_steps_text = """
        **Next Steps:**
        
        1. ✅ **Download your MSP security assessment** using the button above
        2. 📧 **Client follow-up sent** - Your client will receive an email to complete business information
        3. 📊 **Track completion** - You'll receive updates when the client completes their portion
        4. 🔒 **Review security gaps** identified in the assessment
        5. 📞 **Schedule report review consultation** - [Book your SeedPod Cyber consultation here](https://calendly.com/d/crfr-qs3-c6f/seedpod-cyber-insurability-report-review)
        
        **Client Process:**
        - Your client will receive an email with a link to complete their portion
        - They'll provide business information, loss history, and cyber insurance details
        - A second CSV will be generated when they complete their portion
        
        Thank you for completing the MSP Security Assessment!
        
        """
    else:
        next_steps_text = """
        **Next Steps:**
        
        1. ✅ **Download your complete client audit data** using the button above
        2. 📊 **Review the audit summary** for key client security metrics
        3. 📋 **Follow up on identified gaps** in client security posture
        4. 🔒 **Recommend security improvements** based on audit findings
        5. 📞 **Schedule report review consultation** - [Book your SeedPod Cyber consultation here](https://calendly.com/d/crfr-qs3-c6f/seedpod-cyber-insurability-report-review)


        """
        
        if st.session_state.form_data.get('has_cyber_insurance') == 'Yes':
            next_steps_text += "\n    6. 🛡️ **Send cyber insurance policy** to support@seedpodcyber.com"
        
        next_steps_text += "\n\n    Thank you for completing the Complete Client Audit!"
    
    #Commented out stuff -
    """
    IF ------
    **Ready to discuss your results?** 
        Schedule a consultation to review your insurability report and discuss next steps: 
        👉 [SeedPod Cyber Report Review](https://calendly.com/d/crfr-qs3-c6f/seedpod-cyber-insurability-report-review)

    ELSE ------

    **Ready to discuss your results?** 
        Schedule a consultation to review your insurability report and discuss next steps: 
        👉 [SeedPod Cyber Report Review](https://calendly.com/d/crfr-qs3-c6f/seedpod-cyber-insurability-report-review)
    """


    st.info(next_steps_text)
    
    # Option to reset form
    st.markdown("---")
    reset_button_text = "🔄 Start New Assessment" if is_msp_only else "🔄 Start New Client Audit"
    if st.button(reset_button_text, key="reset_audit", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key != 'access_granted':  # Keep access granted
                del st.session_state[key]
        st.rerun()

# Copyright Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666; font-size: 0.9em;">
    Copyright 2025 SeedPod Cyber LLC, All Rights Reserved
</div>
""", unsafe_allow_html=True)


# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import io
# import os
# import base64

# # Configure Streamlit for Azure deployment
# os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
# os.environ['STREAMLIT_SERVER_PORT'] = str(os.environ.get('PORT', '8000'))
# os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
# os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
# os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

# # Load environment variables from .env file for local development
# try:
#     from dotenv import load_dotenv
#     load_dotenv()
# except ImportError:
#     # dotenv not installed, will rely on system environment variables
#     pass

# st.set_page_config(
#     page_title="MSP Client Insurability Audit",
#     page_icon="🛡️",
#     layout="wide"
# )

# # 6-digit NAICS Codes Dictionary - Comprehensive industry codes
# NAICS_CODES = {
#     "111110 - Soybean Farming": "111110",
#     "111120 - Oilseed (except Soybean) Farming": "111120",
#     "111130 - Dry Pea and Bean Farming": "111130",
#     "111140 - Wheat Farming": "111140",
#     "111150 - Corn Farming": "111150",
#     "111160 - Rice Farming": "111160",
#     "111191 - Oilseed and Grain Combination Farming": "111191",
#     "111199 - All Other Grain Farming": "111199",
#     "111211 - Potato Farming": "111211",
#     "111219 - Other Vegetable (except Potato) and Melon Farming": "111219",
#     "111310 - Orange Groves": "111310",
#     "111320 - Citrus (except Orange) Groves": "111320",
#     "111331 - Apple Orchards": "111331",
#     "111332 - Grape Vineyards": "111332",
#     "111333 - Strawberry Farming": "111333",
#     "111334 - Berry (except Strawberry) Farming": "111334",
#     "111335 - Tree Nut Farming": "111335",
#     "111336 - Fruit and Tree Nut Combination Farming": "111336",
#     "111339 - Other Noncitrus Fruit Farming": "111339",
#     "111411 - Mushroom Production": "111411",
#     "111419 - Other Food Crops Grown Under Cover": "111419",
#     "111421 - Nursery and Tree Production": "111421",
#     "111422 - Floriculture Production": "111422",
#     "111910 - Tobacco Farming": "111910",
#     "111920 - Cotton Farming": "111920",
#     "111930 - Sugarcane Farming": "111930",
#     "111940 - Hay Farming": "111940",
#     "111991 - Sugar Beet Farming": "111991",
#     "111992 - Peanut Farming": "111992",
#     "111998 - All Other Miscellaneous Crop Farming": "111998",
#     "112111 - Beef Cattle Ranching and Farming": "112111",
#     "112112 - Cattle Feedlots": "112112",
#     "112120 - Dairy Cattle and Milk Production": "112120",
#     "112130 - Dual-Purpose Cattle Ranching and Farming": "112130",
#     "112210 - Hog and Pig Farming": "112210",
#     "112310 - Chicken Egg Production": "112310",
#     "112320 - Broilers and Other Meat Type Chicken Production": "112320",
#     "112330 - Turkey Production": "112330",
#     "112340 - Poultry Hatcheries": "112340",
#     "112390 - Other Poultry Production": "112390",
#     "112410 - Sheep Farming": "112410",
#     "112420 - Goat Farming": "112420",
#     "112511 - Finfish Farming and Fish Hatcheries": "112511",
#     "112512 - Shellfish Farming": "112512",
#     "112519 - Other Aquaculture": "112519",
#     "112910 - Apiculture": "112910",
#     "112920 - Horse and Other Equine Production": "112920",
#     "112930 - Fur-Bearing Animal and Rabbit Production": "112930",
#     "112990 - All Other Animal Production": "112990",
#     "221110 - Electric Power Generation": "221110",
#     "221121 - Electric Bulk Power Transmission and Control": "221121",
#     "221122 - Electric Power Distribution": "221122",
#     "221210 - Natural Gas Distribution": "221210",
#     "221310 - Water Supply and Irrigation Systems": "221310",
#     "221320 - Sewage Treatment Facilities": "221320",
#     "221330 - Steam and Air-Conditioning Supply": "221330",
#     "236115 - New Single-Family Housing Construction": "236115",
#     "236116 - New Multifamily Housing Construction": "236116",
#     "236117 - New Housing Operative Builders": "236117",
#     "236118 - Residential Remodelers": "236118",
#     "236210 - Industrial Building Construction": "236210",
#     "236220 - Commercial and Institutional Building Construction": "236220",
#     "237110 - Water and Sewer Line and Related Structures Construction": "237110",
#     "237120 - Oil and Gas Pipeline and Related Structures Construction": "237120",
#     "237130 - Power and Communication Line and Related Structures Construction": "237130",
#     "237210 - Land Subdivision": "237210",
#     "237310 - Highway, Street, and Bridge Construction": "237310",
#     "237990 - Other Heavy and Civil Engineering Construction": "237990",
#     "238110 - Poured Concrete Foundation and Structure Contractors": "238110",
#     "238120 - Structural Steel and Precast Concrete Contractors": "238120",
#     "238130 - Framing Contractors": "238130",
#     "238140 - Masonry Contractors": "238140",
#     "238150 - Glass and Glazing Contractors": "238150",
#     "238160 - Roofing Contractors": "238160",
#     "238170 - Siding Contractors": "238170",
#     "238190 - Other Foundation, Structure, and Building Exterior Contractors": "238190",
#     "238210 - Electrical Contractors and Other Wiring Installation Contractors": "238210",
#     "238220 - Plumbing, Heating, and Air-Conditioning Contractors": "238220",
#     "238290 - Other Building Equipment Contractors": "238290",
#     "238310 - Drywall and Insulation Contractors": "238310",
#     "238320 - Painting and Wall Covering Contractors": "238320",
#     "238330 - Flooring Contractors": "238330",
#     "238340 - Tile and Terrazzo Contractors": "238340",
#     "238350 - Finish Carpentry Contractors": "238350",
#     "238390 - Other Building Finishing Contractors": "238390",
#     "238910 - Site Preparation Contractors": "238910",
#     "238990 - All Other Specialty Trade Contractors": "238990",
#     "311111 - Dog and Cat Food Manufacturing": "311111",
#     "311119 - Other Animal Food Manufacturing": "311119",
#     "311211 - Flour Milling": "311211",
#     "311212 - Rice Milling": "311212",
#     "311213 - Malt Manufacturing": "311213",
#     "311221 - Wet Corn Milling": "311221",
#     "311222 - Soybean Processing": "311222",
#     "311223 - Other Oilseed Processing": "311223",
#     "311225 - Fats and Oils Refining and Blending": "311225",
#     "311230 - Breakfast Cereal Manufacturing": "311230",
#     "311311 - Sugarcane Mills": "311311",
#     "311312 - Cane Sugar Refining": "311312",
#     "311313 - Beet Sugar Manufacturing": "311313",
#     "311320 - Chocolate and Confectionery Manufacturing from Cacao Beans": "311320",
#     "311330 - Confectionery Manufacturing from Purchased Chocolate": "311330",
#     "311340 - Nonchocolate Confectionery Manufacturing": "311340",
#     "311351 - Chocolate and Confectionery Manufacturing from Cacao Beans": "311351",
#     "311352 - Confectionery Manufacturing from Purchased Chocolate": "311352",
#     "311411 - Frozen Fruit, Juice, and Vegetable Manufacturing": "311411",
#     "311412 - Frozen Specialty Food Manufacturing": "311412",
#     "311421 - Fruit and Vegetable Canning": "311421",
#     "311422 - Specialty Canning": "311422",
#     "311423 - Dried and Dehydrated Food Manufacturing": "311423",
#     "311511 - Fluid Milk Manufacturing": "311511",
#     "311512 - Creamery Butter Manufacturing": "311512",
#     "311513 - Cheese Manufacturing": "311513",
#     "311514 - Dry, Condensed, and Evaporated Dairy Product Manufacturing": "311514",
#     "311520 - Ice Cream and Frozen Dessert Manufacturing": "311520",
#     "311611 - Animal (except Poultry) Slaughtering": "311611",
#     "311612 - Meat Processed from Carcasses": "311612",
#     "311613 - Rendering and Meat Byproduct Processing": "311613",
#     "311615 - Poultry Processing": "311615",
#     "311711 - Seafood Canning": "311711",
#     "311712 - Fresh and Frozen Seafood Processing": "311712",
#     "311813 - Frozen Cakes, Pies, and Other Pastries Manufacturing": "311813",
#     "311821 - Cookie and Cracker Manufacturing": "311821",
#     "311822 - Flour Mixes and Dough Manufacturing from Purchased Flour": "311822",
#     "311823 - Dry Pasta Manufacturing": "311823",
#     "311830 - Tortilla Manufacturing": "311830",
#     "311911 - Roasted Nuts and Peanut Butter Manufacturing": "311911",
#     "311919 - Other Snack Food Manufacturing": "311919",
#     "311920 - Coffee and Tea Manufacturing": "311920",
#     "311930 - Flavoring Syrup and Concentrate Manufacturing": "311930",
#     "311941 - Mayonnaise, Dressing, and Other Prepared Sauce Manufacturing": "311941",
#     "311942 - Spice and Extract Manufacturing": "311942",
#     "311991 - Perishable Prepared Food Manufacturing": "311991",
#     "311999 - All Other Miscellaneous Food Manufacturing": "311999",
#     "312111 - Soft Drink Manufacturing": "312111",
#     "312112 - Bottled Water Manufacturing": "312112",
#     "312113 - Ice Manufacturing": "312113",
#     "312120 - Breweries": "312120",
#     "312130 - Wineries": "312130",
#     "312140 - Distilleries": "312140",
#     "312210 - Tobacco Stemming and Redrying": "312210",
#     "312221 - Cigarette Manufacturing": "312221",
#     "312229 - Other Tobacco Product Manufacturing": "312229",
#     "423110 - Automobile and Other Motor Vehicle Merchant Wholesalers": "423110",
#     "423120 - Motor Vehicle Supplies and New Parts Merchant Wholesalers": "423120",
#     "423130 - Tire and Tube Merchant Wholesalers": "423130",
#     "423140 - Motor Vehicle Parts (Used) Merchant Wholesalers": "423140",
#     "423210 - Furniture Merchant Wholesalers": "423210",
#     "423220 - Home Furnishing Merchant Wholesalers": "423220",
#     "423310 - Lumber, Plywood, Millwork, and Wood Panel Merchant Wholesalers": "423310",
#     "423320 - Brick, Stone, and Related Construction Material Merchant Wholesalers": "423320",
#     "423330 - Roofing, Siding, and Insulation Material Merchant Wholesalers": "423330",
#     "423390 - Other Construction Material Merchant Wholesalers": "423390",
#     "423410 - Photographic Equipment and Supplies Merchant Wholesalers": "423410",
#     "423420 - Office Equipment Merchant Wholesalers": "423420",
#     "423430 - Computer and Computer Peripheral Equipment and Software Merchant Wholesalers": "423430",
#     "423440 - Other Commercial Equipment Merchant Wholesalers": "423440",
#     "423450 - Medical, Dental, and Hospital Equipment and Supplies Merchant Wholesalers": "423450",
#     "423460 - Ophthalmic Goods Merchant Wholesalers": "423460",
#     "423490 - Other Professional Equipment and Supplies Merchant Wholesalers": "423490",
#     "423510 - Metal Service Centers and Other Metal Merchant Wholesalers": "423510",
#     "423520 - Coal and Other Mineral and Ore Merchant Wholesalers": "423520",
#     "423610 - Electrical Apparatus and Equipment, Wiring Supplies, and Related Equipment Merchant Wholesalers": "423610",
#     "423620 - Electrical and Electronic Appliance, Television, and Radio Set Merchant Wholesalers": "423620",
#     "423690 - Other Electronic Parts and Equipment Merchant Wholesalers": "423690",
#     "423710 - Hardware Merchant Wholesalers": "423710",
#     "423720 - Plumbing and Heating Equipment and Supplies (Hydronics) Merchant Wholesalers": "423720",
#     "423730 - Warm Air Heating and Air-Conditioning Equipment and Supplies Merchant Wholesalers": "423730",
#     "423740 - Refrigeration Equipment and Supplies Merchant Wholesalers": "423740",
#     "423810 - Construction and Mining (except Oil Well) Machinery and Equipment Merchant Wholesalers": "423810",
#     "423820 - Farm and Garden Machinery and Equipment Merchant Wholesalers": "423820",
#     "423830 - Industrial Machinery and Equipment Merchant Wholesalers": "423830",
#     "423840 - Industrial Supplies Merchant Wholesalers": "423840",
#     "423850 - Service Establishment Equipment and Supplies Merchant Wholesalers": "423850",
#     "423860 - Transportation Equipment and Supplies (except Motor Vehicle) Merchant Wholesalers": "423860",
#     "423910 - Sporting and Recreational Goods and Supplies Merchant Wholesalers": "423910",
#     "423920 - Toy and Hobby Goods and Supplies Merchant Wholesalers": "423920",
#     "423930 - Recyclable Material Merchant Wholesalers": "423930",
#     "423940 - Jewelry, Watch, Precious Stone, and Precious Metal Merchant Wholesalers": "423940",
#     "423990 - Other Miscellaneous Durable Goods Merchant Wholesalers": "423990",
#     "441110 - New Car Dealers": "441110",
#     "441120 - Used Car Dealers": "441120",
#     "441210 - Recreational Vehicle Dealers": "441210",
#     "441222 - Boat Dealers": "441222",
#     "441228 - Motorcycle, ATV, and All Other Motor Vehicle Dealers": "441228",
#     "441310 - Automotive Parts and Accessories Stores": "441310",
#     "441320 - Tire Dealers": "441320",
#     "442110 - Furniture Stores": "442110",
#     "442210 - Floor Covering Stores": "442210",
#     "442291 - Window Treatment Stores": "442291",
#     "442299 - All Other Home Furnishings Stores": "442299",
#     "443142 - Electronics Stores": "443142",
#     "443143 - Computer and Software Stores": "443143",
#     "443144 - Camera and Photographic Supplies Stores": "443144",
#     "444110 - Home Centers": "444110",
#     "444120 - Paint and Wallpaper Stores": "444120",
#     "444130 - Hardware Stores": "444130",
#     "444190 - Other Building Material Dealers": "444190",
#     "444220 - Nursery, Garden Center, and Farm Supply Stores": "444220",
#     "445110 - Supermarkets and Other Grocery (except Convenience) Stores": "445110",
#     "445120 - Convenience Stores": "445120",
#     "445210 - Meat Markets": "445210",
#     "445220 - Fish and Seafood Markets": "445220",
#     "445230 - Fruit and Vegetable Markets": "445230",
#     "445291 - Baked Goods Stores": "445291",
#     "445292 - Confectionery and Nut Stores": "445292",
#     "445299 - All Other Specialty Food Stores": "445299",
#     "445310 - Beer, Wine, and Liquor Stores": "445310",
#     "446110 - Pharmacies and Drug Stores": "446110",
#     "446120 - Cosmetics, Beauty Supplies, and Perfume Stores": "446120",
#     "446130 - Optical Goods Stores": "446130",
#     "446191 - Food (Health) Supplement Stores": "446191",
#     "446199 - All Other Health and Personal Care Stores": "446199",
#     "447110 - Gasoline Stations with Convenience Stores": "447110",
#     "447190 - Other Gasoline Stations": "447190",
#     "448110 - Men's Clothing Stores": "448110",
#     "448120 - Women's Clothing Stores": "448120",
#     "448130 - Children's and Infants' Clothing Stores": "448130",
#     "448140 - Family Clothing Stores": "448140",
#     "448150 - Clothing Accessories Stores": "448150",
#     "448190 - Other Clothing Stores": "448190",
#     "448210 - Shoe Stores": "448210",
#     "448310 - Jewelry Stores": "448310",
#     "448320 - Luggage and Leather Goods Stores": "448320",
#     "451110 - Sporting Goods Stores": "451110",
#     "451120 - Hobby, Toy, and Game Stores": "451120",
#     "451130 - Sewing, Needlework, and Piece Goods Stores": "451130",
#     "451140 - Musical Instrument and Supplies Stores": "451140",
#     "451211 - Book Stores": "451211",
#     "451212 - News Dealers and Newsstands": "451212",
#     "452111 - Department Stores (except Discount Department Stores)": "452111",
#     "452112 - Discount Department Stores": "452112",
#     "452210 - Warehouse Clubs and Supercenters": "452210",
#     "452311 - Warehouse Clubs and Supercenters": "452311",
#     "452319 - All Other General Merchandise Stores": "452319",
#     "453110 - Florists": "453110",
#     "453210 - Office Supplies and Stationery Stores": "453210",
#     "453220 - Gift, Novelty, and Souvenir Stores": "453220",
#     "453310 - Used Merchandise Stores": "453310",
#     "453390 - Other Miscellaneous Store Retailers": "453390",
#     "453910 - Pet and Pet Supplies Stores": "453910",
#     "453920 - Art Dealers": "453920",
#     "453930 - Mobile Home Dealers": "453930",
#     "453991 - Tobacco Stores": "453991",
#     "453998 - All Other Miscellaneous Store Retailers (except Tobacco Stores)": "453998",
#     "454110 - Electronic Shopping and Mail-Order Houses": "454110",
#     "454210 - Vending Machine Operators": "454210",
#     "454310 - Fuel Dealers": "454310",
#     "454390 - Other Direct Selling Establishments": "454390",
#     "511110 - Newspaper Publishers": "511110",
#     "511120 - Periodical Publishers": "511120",
#     "511130 - Book Publishers": "511130",
#     "511140 - Directory and Mailing List Publishers": "511140",
#     "511191 - Greeting Card Publishers": "511191",
#     "511199 - All Other Publishers": "511199",
#     "511210 - Software Publishers": "511210",
#     "517110 - Wired Telecommunications Carriers": "517110",
#     "517210 - Wireless Telecommunications Carriers (except Satellite)": "517210",
#     "517311 - Wired Telecommunications Carriers": "517311",
#     "517312 - Wireless Telecommunications Carriers (except Satellite)": "517312",
#     "517410 - Satellite Telecommunications": "517410",
#     "517510 - Cable and Other Subscription Programming": "517510",
#     "517910 - Other Telecommunications": "517910",
#     "518111 - Internet Service Providers": "518111",
#     "518112 - Web Search Portals": "518112",
#     "518210 - Data Processing, Hosting, and Related Services": "518210",
#     "519110 - News Syndicates": "519110",
#     "519120 - Libraries and Archives": "519120",
#     "519190 - All Other Information Services": "519190",
#     "522110 - Commercial Banking": "522110",
#     "522120 - Savings Institutions": "522120",
#     "522130 - Credit Unions": "522130",
#     "522190 - Other Depository Credit Intermediation": "522190",
#     "522210 - Credit Card Issuing": "522210",
#     "522220 - Sales Financing": "522220",
#     "522291 - Consumer Lending": "522291",
#     "522292 - Real Estate Credit": "522292",
#     "522293 - International Trade Financing": "522293",
#     "522294 - Secondary Market Financing": "522294",
#     "522298 - All Other Nondepository Credit Intermediation": "522298",
#     "522310 - Mortgage and Nonmortgage Loan Brokers": "522310",
#     "522320 - Financial Transactions Processing, Reserve, and Clearinghouse Activities": "522320",
#     "522390 - Other Activities Related to Credit Intermediation": "522390",
#     "523110 - Investment Banking and Securities Dealing": "523110",
#     "523120 - Securities Brokerage": "523120",
#     "523130 - Commodity Contracts Dealing": "523130",
#     "523140 - Commodity Contracts Brokerage": "523140",
#     "523210 - Securities and Commodity Exchanges": "523210",
#     "523910 - Miscellaneous Intermediation": "523910",
#     "523920 - Portfolio Management": "523920",
#     "523930 - Investment Advice": "523930",
#     "523991 - Trust, Fiduciary, and Custody Activities": "523991",
#     "523999 - Miscellaneous Financial Investment Activities": "523999",
#     "524113 - Direct Life Insurance Carriers": "524113",
#     "524114 - Direct Health and Medical Insurance Carriers": "524114",
#     "524126 - Direct Property and Casualty Insurance Carriers": "524126",
#     "524127 - Direct Title Insurance Carriers": "524127",
#     "524128 - Other Direct Insurance (except Life, Health, and Medical) Carriers": "524128",
#     "524130 - Reinsurance Carriers": "524130",
#     "524210 - Insurance Agencies and Brokerages": "524210",
#     "524291 - Claims Adjusting": "524291",
#     "524292 - Third Party Administration of Insurance and Pension Funds": "524292",
#     "524298 - All Other Insurance Related Activities": "524298",
#     "531110 - Lessors of Residential Buildings and Dwellings": "531110",
#     "531120 - Lessors of Nonresidential Buildings (except Miniwarehouses)": "531120",
#     "531130 - Lessors of Miniwarehouses and Self-Storage Units": "531130",
#     "531190 - Lessors of Other Real Estate Property": "531190",
#     "531210 - Offices of Real Estate Agents and Brokers": "531210",
#     "531311 - Residential Property Managers": "531311",
#     "531312 - Nonresidential Property Managers": "531312",
#     "531320 - Offices of Real Estate Appraisers": "531320",
#     "531390 - Other Activities Related to Real Estate": "531390",
#     "532111 - Passenger Car Rental": "532111",
#     "532112 - Passenger Car Leasing": "532112",
#     "532120 - Truck, Utility Trailer, and RV (Recreational Vehicle) Rental and Leasing": "532120",
#     "532210 - Consumer Electronics and Appliances Rental": "532210",
#     "532220 - Formal Wear and Costume Rental": "532220",
#     "532230 - Video Tape and Disc Rental": "532230",
#     "532290 - Other Consumer Goods Rental": "532290",
#     "532310 - General Rental Centers": "532310",
#     "532411 - Commercial Air, Rail, and Water Transportation Equipment Rental and Leasing": "532411",
#     "532412 - Construction, Mining, and Forestry Machinery and Equipment Rental and Leasing": "532412",
#     "532420 - Office Machinery and Equipment Rental and Leasing": "532420",
#     "541110 - Offices of Lawyers": "541110",
#     "541191 - Title Abstract and Settlement Offices": "541191",
#     "541199 - All Other Legal Services": "541199",
#     "541211 - Offices of Certified Public Accountants": "541211",
#     "541213 - Tax Preparation Services": "541213",
#     "541214 - Payroll Services": "541214",
#     "541219 - Other Accounting Services": "541219",
#     "541310 - Architectural Services": "541310",
#     "541320 - Landscape Architectural Services": "541320",
#     "541330 - Engineering Services": "541330",
#     "541340 - Drafting Services": "541340",
#     "541350 - Building Inspection Services": "541350",
#     "541360 - Geophysical Surveying and Mapping Services": "541360",
#     "541370 - Surveying and Mapping (except Geophysical) Services": "541370",
#     "541380 - Testing Laboratories": "541380",
#     "541410 - Interior Design Services": "541410",
#     "541420 - Industrial Design Services": "541420",
#     "541430 - Graphic Design Services": "541430",
#     "541490 - Other Specialized Design Services": "541490",
#     "541511 - Custom Computer Programming Services": "541511",
#     "541512 - Computer Systems Design Services": "541512",
#     "541513 - Computer Facilities Management Services": "541513",
#     "541519 - Other Computer Related Services": "541519",
#     "541611 - Administrative Management and General Management Consulting Services": "541611",
#     "541612 - Human Resources Consulting Services": "541612",
#     "541613 - Marketing Consulting Services": "541613",
#     "541614 - Process, Physical Distribution, and Logistics Consulting Services": "541614",
#     "541618 - Other Management Consulting Services": "541618",
#     "541620 - Environmental Consulting Services": "541620",
#     "541690 - Other Scientific and Technical Consulting Services": "541690",
#     "541711 - Research and Development in Biotechnology": "541711",
#     "541712 - Research and Development in the Physical, Engineering, and Life Sciences (except Biotechnology)": "541712",
#     "541720 - Research and Development in the Social Sciences and Humanities": "541720",
#     "541810 - Advertising Agencies": "541810",
#     "541820 - Public Relations Agencies": "541820",
#     "541830 - Media Buying Agencies": "541830",
#     "541840 - Media Representatives": "541840",
#     "541850 - Outdoor Advertising": "541850",
#     "541860 - Direct Mail Advertising": "541860",
#     "541870 - Advertising Material Distribution Services": "541870",
#     "541890 - Other Services Related to Advertising": "541890",
#     "541910 - Marketing Research and Public Opinion Polling": "541910",
#     "541921 - Photography Studios, Portrait": "541921",
#     "541922 - Commercial Photography": "541922",
#     "541930 - Translation and Interpretation Services": "541930",
#     "541940 - Veterinary Services": "541940",
#     "541990 - All Other Professional, Scientific, and Technical Services": "541990",
#     "561110 - Office Administrative Services": "561110",
#     "561210 - Facilities Support Services": "561210",
#     "561310 - Employment Placement Agencies": "561310",
#     "561320 - Temporary Help Services": "561320",
#     "561330 - Professional Employer Organizations": "561330",
#     "561410 - Document Preparation Services": "561410",
#     "561421 - Telephone Answering Services": "561421",
#     "561422 - Telemarketing Bureaus and Other Contact Centers": "561422",
#     "561431 - Private Mail Centers": "561431",
#     "561439 - Other Business Service Centers (including Copy Shops)": "561439",
#     "561440 - Collection Agencies": "561440",
#     "561450 - Credit Bureaus": "561450",
#     "561490 - Other Business Support Services": "561490",
#     "561510 - Travel Agencies": "561510",
#     "561520 - Tour Operators": "561520",
#     "561591 - Convention and Visitors Bureaus": "561591",
#     "561599 - All Other Travel Arrangement and Reservation Services": "561599",
#     "561611 - Investigation Services": "561611",
#     "561612 - Security Guards and Patrol Services": "561612",
#     "561613 - Armored Car Services": "561613",
#     "561621 - Security Systems Services (except Locksmiths)": "561621",
#     "561622 - Locksmiths": "561622",
#     "561710 - Exterminating and Pest Control Services": "561710",
#     "561720 - Janitorial Services": "561720",
#     "561730 - Landscaping Services": "561730",
#     "561740 - Carpet and Upholstery Cleaning Services": "561740",
#     "561790 - Other Services to Buildings and Dwellings": "561790",
#     "561910 - Packaging and Labeling Services": "561910",
#     "561920 - Convention and Trade Show Organizers": "561920",
#     "561990 - All Other Support Services": "561990",
#     "611110 - Elementary and Secondary Schools": "611110",
#     "611210 - Junior Colleges": "611210",
#     "611310 - Colleges, Universities, and Professional Schools": "611310",
#     "611410 - Business and Secretarial Schools": "611410",
#     "611420 - Computer Training": "611420",
#     "611430 - Professional and Management Development Training": "611430",
#     "611511 - Cosmetology and Barber Schools": "611511",
#     "611512 - Flight Training": "611512",
#     "611513 - Apprenticeship Training": "611513",
#     "611519 - Other Technical and Trade Schools": "611519",
#     "611610 - Fine Arts Schools": "611610",
#     "611620 - Sports and Recreation Instruction": "611620",
#     "611630 - Language Schools": "611630",
#     "611691 - Exam Preparation and Tutoring": "611691",
#     "611692 - Automobile Driving Schools": "611692",
#     "611699 - All Other Miscellaneous Schools and Instruction": "611699",
#     "611710 - Educational Support Services": "611710",
#     "621111 - Offices of Physicians (except Mental Health Specialists)": "621111",
#     "621112 - Offices of Physicians, Mental Health Specialists": "621112",
#     "621210 - Offices of Dentists": "621210",
#     "621310 - Offices of Chiropractors": "621310",
#     "621320 - Offices of Optometrists": "621320",
#     "621330 - Offices of Mental Health Practitioners (except Physicians)": "621330",
#     "621340 - Offices of Physical, Occupational and Speech Therapists, and Audiologists": "621340",
#     "621391 - Offices of Podiatrists": "621391",
#     "621399 - Offices of All Other Miscellaneous Health Practitioners": "621399",
#     "621410 - Family Planning Centers": "621410",
#     "621420 - Outpatient Mental Health and Substance Abuse Centers": "621420",
#     "621491 - HMO Medical Centers": "621491",
#     "621492 - Kidney Dialysis Centers": "621492",
#     "621493 - Freestanding Ambulatory Surgical and Emergency Centers": "621493",
#     "621498 - All Other Outpatient Care Centers": "621498",
#     "621511 - Medical Laboratories": "621511",
#     "621512 - Diagnostic Imaging Centers": "621512",
#     "621610 - Home Health Care Services": "621610",
#     "621910 - Ambulance Services": "621910",
#     "621991 - Blood and Organ Banks": "621991",
#     "621999 - All Other Miscellaneous Ambulatory Health Care Services": "621999",
#     "622110 - General Medical and Surgical Hospitals": "622110",
#     "622210 - Psychiatric and Substance Abuse Hospitals": "622210",
#     "622310 - Specialty (except Psychiatric and Substance Abuse) Hospitals": "622310",
#     "623110 - Nursing Care Facilities (Skilled Nursing Facilities)": "623110",
#     "623210 - Residential Intellectual and Developmental Disability Facilities": "623210",
#     "623220 - Residential Mental Health and Substance Abuse Facilities": "623220",
#     "623311 - Continuing Care Retirement Communities": "623311",
#     "623312 - Assisted Living Facilities for the Elderly": "623312",
#     "623990 - Other Residential Care Facilities": "623990",
#     "624110 - Child and Youth Services": "624110",
#     "624120 - Services for the Elderly and Persons with Disabilities": "624120",
#     "624190 - Other Individual and Family Services": "624190",
#     "624210 - Community Food Services": "624210",
#     "624221 - Temporary Shelters": "624221",
#     "624229 - Other Community Housing Services": "624229",
#     "624230 - Emergency and Other Relief Services": "624230",
#     "624310 - Vocational Rehabilitation Services": "624310",
#     "624410 - Child Day Care Services": "624410",
#     "711110 - Theater Companies and Dinner Theaters": "711110",
#     "711120 - Dance Companies": "711120",
#     "711130 - Musical Groups and Artists": "711130",
#     "711190 - Other Performing Arts Companies": "711190",
#     "711211 - Sports Teams and Clubs": "711211",
#     "711212 - Racetracks": "711212",
#     "711219 - Other Spectator Sports": "711219",
#     "711310 - Promoters of Performing Arts, Sports, and Similar Events with Facilities": "711310",
#     "711320 - Promoters of Performing Arts, Sports, and Similar Events without Facilities": "711320",
#     "711410 - Agents and Managers for Artists, Athletes, Entertainers, and Other Public Figures": "711410",
#     "711510 - Independent Artists, Writers, and Performers": "711510",
#     "712110 - Museums": "712110",
#     "712120 - Historical Sites": "712120",
#     "712130 - Zoos and Botanical Gardens": "712130",
#     "712190 - Nature Parks and Other Similar Institutions": "712190",
#     "713110 - Amusement and Theme Parks": "713110",
#     "713120 - Amusement Arcades": "713120",
#     "713210 - Casinos (except Casino Hotels)": "713210",
#     "713290 - Other Gambling Industries": "713290",
#     "713910 - Golf Courses and Country Clubs": "713910",
#     "713920 - Skiing Facilities": "713920",
#     "713930 - Marinas": "713930",
#     "713940 - Fitness and Recreational Sports Centers": "713940",
#     "713950 - Bowling Centers": "713950",
#     "713990 - All Other Amusement and Recreation Industries": "713990",
#     "721110 - Hotels (except Casino Hotels) and Motels": "721110",
#     "721120 - Casino Hotels": "721120",
#     "721191 - Bed and Breakfast Inns": "721191",
#     "721199 - All Other Traveler Accommodation": "721199",
#     "721214 - Recreational and Vacation Camps (except Campgrounds)": "721214",
#     "721211 - RV (Recreational Vehicle) Parks and Campgrounds": "721211",
#     "722110 - Full-Service Restaurants": "722110",
#     "722211 - Limited-Service Restaurants": "722211",
#     "722212 - Cafeterias, Grill Buffets, and Buffets": "722212",
#     "722213 - Snack and Nonalcoholic Beverage Bars": "722213",
#     "722310 - Food Service Contractors": "722310",
#     "722320 - Caterers": "722320",
#     "722330 - Mobile Food Services": "722330",
#     "722410 - Drinking Places (Alcoholic Beverages)": "722410",
#     "811111 - General Automotive Repair": "811111",
#     "811112 - Automotive Exhaust System Repair": "811112",
#     "811113 - Automotive Transmission Repair": "811113",
#     "811118 - Other Automotive Mechanical and Electrical Repair and Maintenance": "811118",
#     "811121 - Automotive Body, Paint, and Upholstery Repair and Maintenance": "811121",
#     "811122 - Automotive Glass Replacement Shops": "811122",
#     "811191 - Automotive Oil Change and Lubrication Shops": "811191",
#     "811192 - Car Washes": "811192",
#     "811198 - All Other Automotive Repair and Maintenance": "811198",
#     "811211 - Consumer Electronics Repair and Maintenance": "811211",
#     "811212 - Computer and Office Machine Repair and Maintenance": "811212",
#     "811213 - Communication Equipment Repair and Maintenance": "811213",
#     "811219 - Other Electronic and Precision Equipment Repair and Maintenance": "811219",
#     "811310 - Commercial and Industrial Machinery and Equipment (except Automotive and Electronic) Repair and Maintenance": "811310",
#     "811411 - Home and Garden Equipment Repair and Maintenance": "811411",
#     "811412 - Appliance Repair and Maintenance": "811412",
#     "811420 - Reupholstery and Furniture Repair": "811420",
#     "811430 - Footwear and Leather Goods Repair": "811430",
#     "811490 - Other Personal and Household Goods Repair and Maintenance": "811490",
#     "812111 - Barber Shops": "812111",
#     "812112 - Beauty Salons": "812112",
#     "812113 - Nail Salons": "812113",
#     "812191 - Diet and Weight Reducing Centers": "812191",
#     "812199 - Other Personal Care Services": "812199",
#     "812210 - Funeral Homes and Funeral Services": "812210",
#     "812220 - Cemeteries and Crematories": "812220",
#     "812310 - Coin-Operated Laundries and Drycleaners": "812310",
#     "812320 - Drycleaning and Laundry Services (except Coin-Operated)": "812320",
#     "812331 - Linen Supply": "812331",
#     "812332 - Industrial Launderers": "812332",
#     "812910 - Pet Care (except Veterinary) Services": "812910",
#     "812921 - Photofinishing Laboratories (except One-Hour)": "812921",
#     "812922 - One-Hour Photofinishing": "812922",
#     "812930 - Parking Lots and Garages": "812930",
#     "812990 - All Other Personal Services": "812990",
#     "813110 - Religious Organizations": "813110",
#     "813211 - Grantmaking Foundations": "813211",
#     "813212 - Voluntary Health Organizations": "813212",
#     "813219 - Other Grantmaking and Giving Services": "813219",
#     "813311 - Human Rights Organizations": "813311",
#     "813312 - Environment, Conservation and Wildlife Organizations": "813312",
#     "813319 - Other Social Advocacy Organizations": "813319",
#     "813410 - Civic and Social Organizations": "813410",
#     "813910 - Business Associations": "813910",
#     "813920 - Professional Organizations": "813920",
#     "813930 - Labor Unions and Similar Labor Organizations": "813930",
#     "813940 - Political Organizations": "813940",
#     "813990 - Other Similar Organizations (except Business, Professional, Labor, and Political Organizations)": "813990"
# }

# def send_assessment_email(csv_data, filename, assessment_type, form_data):
#     """Send assessment CSV via SendGrid email"""
#     try:
#         from sendgrid import SendGridAPIClient
#         from sendgrid.helpers.mail import Mail, Attachment
        
#         sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
#         if not sendgrid_api_key:
#             st.error("❌ Email service not configured. SENDGRID_API_KEY environment variable not set.")
#             return False
        
#         sg = SendGridAPIClient(api_key=sendgrid_api_key)
        
#         subject = f"MSP Client Audit - {assessment_type} - {form_data.get('organization_name', 'Unknown Client')}"
        
#         # Add cyber insurance info to email
#         cyber_insurance_info = ""
#         if form_data.get('has_cyber_insurance') == 'Yes':
#             cyber_insurance_info = f"""
#             <p><strong>Cyber Insurance:</strong> Yes (Effective: {form_data.get('cyber_insurance_effective_date', 'N/A')})</p>
#             <p><strong>⚠️ ACTION REQUIRED:</strong> Please send a copy of the client's cyber insurance policy to support@seedpodcyber.com</p>
#             """
#         else:
#             cyber_insurance_info = "<p><strong>Cyber Insurance:</strong> No</p>"
        
#         html_content = f"""
#         <h2>New MSP Client Insurability Audit Submission</h2>
#         <p><strong>Assessment Type:</strong> {assessment_type}</p>
#         <p><strong>Client Organization:</strong> {form_data.get('organization_name', 'N/A')}</p>
#         <p><strong>Contact:</strong> {form_data.get('first_name', '')} {form_data.get('last_name', '')}</p>
#         <p><strong>Email:</strong> {form_data.get('email', 'N/A')}</p>
#         <p><strong>MSP:</strong> {form_data.get('msp_name', 'N/A')}</p>
#         <p><strong>Submission Date:</strong> {form_data.get('submission_date', 'N/A')}</p>
#         {cyber_insurance_info}
        
#         <p>Please find the detailed client audit data attached as a CSV file.</p>
        
#         <hr>
#         <p><em>This audit was submitted through the MSP Client Insurability Assessment platform.</em></p>
#         """
        
#         message = Mail(
#             from_email='noreply@seedpodcyber.com',
#             to_emails='support@seedpodcyber.com',
#             subject=subject,
#             html_content=html_content
#         )
        
#         encoded_csv = base64.b64encode(csv_data.encode()).decode()
#         attachment = Attachment(
#             file_content=encoded_csv,
#             file_type="text/csv",
#             file_name=filename,
#             disposition="attachment"
#         )
#         message.attachment = attachment
        
#         response = sg.send(message)
#         return response.status_code == 202
        
#     except ImportError:
#         st.error("❌ SendGrid not installed. Please run: pip install sendgrid")
#         return False
#     except Exception as e:
#         st.error(f"❌ Email sending failed: {str(e)}")
#         return False

# def create_tooltip(question_text, tooltip_text):
#     """Create a question with tooltip functionality"""
#     return f"""
#     <div class="question-with-tooltip">
#         <span class="question-text">{question_text}</span>
#         <div class="tooltip">ℹ️
#             <span class="tooltiptext">{tooltip_text}</span>
#         </div>
#     </div>
#     """

# def format_currency(amount):
#     """Format number as currency with commas and no decimals"""
#     if amount == 0:
#         return "$0"
#     return f"${amount:,.0f}"

# def display_currency_input(label, key, help_text="", tooltip_text=""):
#     """Display currency input with live formatting"""
#     if tooltip_text:
#         st.markdown(create_tooltip(label, tooltip_text), unsafe_allow_html=True)
#     else:
#         st.markdown(f"**{label}**")
    
#     # Input with proper formatting
#     value = st.number_input(
#         f"Amount in USD",
#         min_value=0,
#         key=key,
#         step=1000,
#         value=0,
#         help=help_text,
#         label_visibility="collapsed"
#     )
    
#     # Display formatted currency immediately below input
#     if value > 0:
#         st.markdown(f"<div style='color: #009D4F; font-weight: bold; font-size: 1.1em; margin-top: -10px; margin-bottom: 15px;'>💰 {format_currency(value)}</div>", unsafe_allow_html=True)
    
#     return value

# # Access Control System
# def check_access():
#     """Check if user has entered valid access key"""
#     if 'access_granted' not in st.session_state:
#         st.session_state.access_granted = False
    
#     if not st.session_state.access_granted:
#         # SeedPod Logo for login page
#         try:
#             st.markdown('<div style="text-align: center; margin: 2rem 0;">', unsafe_allow_html=True)
#             st.image('seedpod_logo.png', width=400)
#             st.markdown('</div>', unsafe_allow_html=True)
#         except:
#             st.markdown("""
#             <div style="text-align: center; margin: 2rem 0;">
#                 <div style="display: inline-block; padding: 1rem 2rem; border: 3px solid #009D4F; border-radius: 10px;">
#                     <h1 style="color: #009D4F; font-size: 2.5rem; font-weight: 800; margin: 0;">SeedPod</h1>
#                     <h2 style="color: #013220; font-size: 1.5rem; font-weight: 600; margin: 0;">CYBER</h2>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)
        
#         # Access key login form
#         st.markdown("""
#         <div style="max-width: 500px; margin: 2rem auto; padding: 2rem; border: 2px solid #009D4F; border-radius: 10px; background: #F8F9FA;">
#             <h2 style="color: #013220; text-align: center; margin-bottom: 1rem;">🛡️ Client Audit Access Required</h2>
#             <p style="text-align: center; color: #666; margin-bottom: 2rem;">
#                 Please enter your access key to continue to the MSP Client Insurability Audit.
#             </p>
#         </div>
#         """, unsafe_allow_html=True)
        
#         # Access key input
#         col1, col2, col3 = st.columns([1, 2, 1])
#         with col2:
#             access_key = st.text_input(
#                 "Access Key:",
#                 type="password",
#                 placeholder="Enter your access key",
#                 help="Contact support@seedpodcyber.com if you need an access key"
#             )
            
#             if st.button("🚀 Access Client Audit", use_container_width=True, type="primary"):
#                 # Check access key against environment variable
#                 valid_key = os.getenv('CLIENT_ACCESS_KEY', 'seedpod2025client')  # Default for testing
                
#                 if access_key == valid_key:
#                     st.session_state.access_granted = True
#                     st.success("✅ Access granted! Redirecting...")
#                     st.rerun()
#                 elif access_key:
#                     st.error("❌ Invalid access key. Please check your key and try again.")
#                     st.info("💡 Contact support@seedpodcyber.com if you need assistance.")
#                 else:
#                     st.warning("⚠️ Please enter an access key.")
        
#         # Contact information
#         st.markdown("---")
#         st.markdown("""
#         <div style="text-align: center; color: #666; font-size: 0.9em;">
#             <p><strong>Need an access key?</strong></p>
#             <p>Contact: <a href="mailto:support@seedpodcyber.com">support@seedpodcyber.com</a></p>
#             <p>This client audit tool is available to authorized MSPs and their clients.</p>
#         </div>
#         """, unsafe_allow_html=True)
        
#         # Copyright
#         st.markdown("---")
#         st.markdown("""
#         <div style="text-align: center; padding: 1rem; color: #666; font-size: 0.9em;">
#             Copyright 2025 SeedPod Cyber LLC, All Rights Reserved
#         </div>
#         """, unsafe_allow_html=True)
        
#         return False
    
#     return True

# # Enhanced CSS with SeedPod branding
# st.markdown("""
# <style>
# /* SeedPod Color Palette: #009D4F, #353535, #013220, #E8E9F3, #EAE0CC */

# .main-header {
#     background: #009D4F;
#     color: white;
#     padding: 2rem;
#     border-radius: 10px;
#     text-align: center;
#     margin-bottom: 2rem;
#     box-shadow: 0 4px 15px rgba(0, 157, 79, 0.3);
# }

# .section-header {
#     background: #E8E9F3;
#     padding: 1rem;
#     border-left: 4px solid #009D4F;
#     margin: 1rem 0;
#     border-radius: 5px;
#     color: #353535;
#     box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
# }

# .section-header h2 {
#     color: #013220;
#     margin-bottom: 0.5rem;
# }

# .loss-history {
#     background: #E8E9F3;
#     padding: 1rem;
#     border-radius: 5px;
#     border: 2px solid #353535;
#     box-shadow: 0 2px 8px rgba(53, 53, 53, 0.2);
# }

# .loss-history h2 {
#     color: #013220;
#     margin-bottom: 0.5rem;
# }

# .security-controls {
#     background: #EAE0CC;
#     padding: 1rem;
#     border-radius: 5px;
#     border: 2px solid #009D4F;
#     box-shadow: 0 2px 8px rgba(0, 157, 79, 0.2);
# }

# .security-controls h2 {
#     color: #013220;
#     margin-bottom: 0.5rem;
# }

# .cyber-insurance {
#     background: #E8F5E8;
#     padding: 1rem;
#     border-radius: 5px;
#     border: 2px solid #009D4F;
#     box-shadow: 0 2px 8px rgba(0, 157, 79, 0.2);
# }

# .cyber-insurance h2 {
#     color: #013220;
#     margin-bottom: 0.5rem;
# }

# .question-examples {
#     background: rgba(0, 157, 79, 0.1);
#     border-left: 3px solid #009D4F;
#     padding: 10px 15px;
#     margin: 10px 0;
#     font-size: 0.9em;
#     color: #353535;
#     border-radius: 5px;
# }

# .stButton > button {
#     background: #009D4F;
#     color: white;
#     border: none;
#     border-radius: 8px;
#     font-weight: 600;
#     transition: all 0.3s ease;
# }

# .stButton > button:hover {
#     background: #013220;
#     box-shadow: 0 4px 15px rgba(0, 157, 79, 0.4);
#     transform: translateY(-2px);
# }

# .stFormSubmitButton > button {
#     background: #009D4F;
#     color: white;
#     border: none;
#     border-radius: 8px;
#     font-weight: 600;
#     padding: 0.75rem 2rem;
#     font-size: 1.1rem;
# }

# .stFormSubmitButton > button:hover {
#     background: #013220;
#     box-shadow: 0 4px 15px rgba(0, 157, 79, 0.4);
# }

# .stDownloadButton > button {
#     background: #009D4F;
#     color: white;
#     border: none;
#     border-radius: 8px;
#     font-weight: 600;
#     font-size: 1.1rem;
#     padding: 0.75rem;
# }

# .stDownloadButton > button:hover {
#     background: #013220;
#     box-shadow: 0 4px 15px rgba(0, 157, 79, 0.4);
# }

# /* Tooltip Styles */
# .tooltip {
#     position: relative;
#     display: inline-block;
#     cursor: help;
#     color: #009D4F;
#     font-weight: bold;
#     margin-left: 5px;
# }

# .tooltip .tooltiptext {
#     visibility: hidden;
#     width: 300px;
#     background-color: #353535;
#     color: white;
#     text-align: left;
#     border-radius: 8px;
#     padding: 12px;
#     position: absolute;
#     z-index: 1000;
#     bottom: 125%;
#     left: 50%;
#     margin-left: -150px;
#     opacity: 0;
#     transition: opacity 0.3s;
#     font-size: 0.9em;
#     line-height: 1.4;
#     box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
#     border: 1px solid #009D4F;
# }

# .tooltip .tooltiptext::after {
#     content: "";
#     position: absolute;
#     top: 100%;
#     left: 50%;
#     margin-left: -5px;
#     border-width: 5px;
#     border-style: solid;
#     border-color: #353535 transparent transparent transparent;
# }

# .tooltip:hover .tooltiptext {
#     visibility: visible;
#     opacity: 1;
# }

# .question-with-tooltip {
#     display: flex;
#     align-items: center;
#     margin-bottom: 10px;
# }

# .question-text {
#     flex-grow: 1;
# }
# </style>
# """, unsafe_allow_html=True)

# # Check access before showing any content
# if not check_access():
#     st.stop()  # Stop execution if access not granted

# # Add logout option in sidebar
# with st.sidebar:
#     st.markdown("---")
#     if st.button("🚪 Logout", help="Clear access and return to login"):
#         st.session_state.access_granted = False
#         st.session_state.clear()  # Clear all session state
#         st.rerun()

# # SeedPod Logo for main page
# try:
#     st.markdown('<div style="text-align: center; margin: 2rem 0;">', unsafe_allow_html=True)
#     st.image('seedpod_logo.png', width=400)
#     st.markdown('</div>', unsafe_allow_html=True)
# except:
#     st.markdown("""
#     <div style="text-align: center; margin: 2rem 0;">
#         <div style="display: inline-block; padding: 1rem 2rem; border: 3px solid #009D4F; border-radius: 10px;">
#             <h1 style="color: #009D4F; font-size: 2.5rem; font-weight: 800; margin: 0;">SeedPod</h1>
#             <h2 style="color: #013220; font-size: 1.5rem; font-weight: 600; margin: 0;">CYBER</h2>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# st.markdown("""
# <div class="main-header">
#     <h1>🛡️ MSP Client Insurability Audit</h1>
#     <h3>Cybersecurity Risk Assessment for MSP Clients</h3>
#     <p>Complete assessment of client security posture and controls</p>
# </div>
# """, unsafe_allow_html=True)

# with st.form("client_audit_form"):
#     # Basic Client Information
#     st.markdown('<div class="section-header"><h2>👤 Client Information</h2><p>Basic details about the client organization</p></div>', unsafe_allow_html=True)
    
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.markdown(create_tooltip(
#             "First Name *",
#             "Enter the first name of the primary contact person for this client organization."
#         ), unsafe_allow_html=True)
#         first_name = st.text_input("First Name", key="first_name", label_visibility="collapsed")
        
#         st.markdown(create_tooltip(
#             "Last Name *",
#             "Enter the last name of the primary contact person for this client organization."
#         ), unsafe_allow_html=True)
#         last_name = st.text_input("Last Name", key="last_name", label_visibility="collapsed")
        
#         st.markdown(create_tooltip(
#             "Email Address *",
#             "Enter the email address of the primary contact person for follow-up communications."
#         ), unsafe_allow_html=True)
#         email = st.text_input("Email", key="email", label_visibility="collapsed")
    
#     with col2:
#         st.markdown(create_tooltip(
#             "Organization Name *",
#             "Enter the legal business name of the client organization as it appears on official documents."
#         ), unsafe_allow_html=True)
#         organization_name = st.text_input("Organization Name", key="organization_name", label_visibility="collapsed")
        
#         st.markdown(create_tooltip(
#             "Organization Address *",
#             "Enter the complete address including Street, City, State and Zip Code of the client organization."
#         ), unsafe_allow_html=True)
#         org_address = st.text_area("Organization Address", key="org_address", label_visibility="collapsed")
        
#         st.markdown(create_tooltip(
#             "Organization Website *",
#             "Enter the website URL for the client organization (e.g., https://example.com)."
#         ), unsafe_allow_html=True)
#         org_website = st.text_input("Organization Website", key="org_website", placeholder="https://", label_visibility="collapsed")
    
#     with col3:
#         st.markdown(create_tooltip(
#             "NAICS Code *",
#             "North American Industry Classification System code that identifies the client's primary business activity. This helps assess industry-specific risks. Search by industry name or enter the 6-digit code."
#         ), unsafe_allow_html=True)
        
#         # Create searchable NAICS code selectbox
#         naics_options = [""] + list(NAICS_CODES.keys())
#         selected_naics = st.selectbox(
#             "NAICS Code", 
#             options=naics_options,
#             key="naics_code",
#             label_visibility="collapsed",
#             help="Start typing to search for your industry"
#         )
        
#         # Extract just the code from the selection
#         if selected_naics:
#             naics_code = NAICS_CODES[selected_naics]
#         else:
#             naics_code = ""
        
#         st.markdown(create_tooltip(
#             "Year of Establishment *",
#             "The year the client organization was founded or incorporated."
#         ), unsafe_allow_html=True)
#         year_established = st.number_input("Year of Establishment", min_value=1900, max_value=2025, key="year_established", label_visibility="collapsed")
        
#         st.markdown(create_tooltip(
#             "Total Number of Employees *",
#             "Enter the total number of employees in the client organization, including full-time and part-time staff."
#         ), unsafe_allow_html=True)
#         total_employees = st.number_input("Total Employees", min_value=1, key="total_employees", label_visibility="collapsed")
    
#     # Revenue Information
#     col4, col5 = st.columns(2)
#     with col4:
#         expected_revenue = display_currency_input(
#             "Expected Revenue for This Fiscal Year *",
#             "expected_revenue",
#             "Enter the expected revenue for the current fiscal year rounded to the nearest whole number",
#             "Expected total gross revenue for the client's current fiscal year. This helps assess the organization's size and risk profile."
#         )
    
#     with col5:
#         st.markdown(create_tooltip(
#             "Name of Managed Service Provider *",
#             "Enter the name of the MSP providing services to this client organization."
#         ), unsafe_allow_html=True)
#         msp_name = st.text_input("MSP Name", key="msp_name", label_visibility="collapsed")
    
#     # Cyber Insurance Section
#     st.markdown('<div class="cyber-insurance"><h2>🛡️ Cyber Insurance Information</h2><p>Information about the client\'s current cyber insurance coverage</p></div>', unsafe_allow_html=True)
    
#     col_insurance1, col_insurance2 = st.columns(2)
    
#     with col_insurance1:
#         st.markdown(create_tooltip(
#             "Does your client organization currently have cyber insurance? *",
#             "Cyber insurance (also called cyber liability insurance) covers financial losses from cyber incidents like data breaches, ransomware attacks, and business interruption due to cyber events."
#         ), unsafe_allow_html=True)
#         has_cyber_insurance = st.radio("Cyber Insurance Status", ["No", "Yes"], key="has_cyber_insurance", label_visibility="collapsed")
    
#     with col_insurance2:
#         if has_cyber_insurance == "Yes":
#             st.markdown(create_tooltip(
#                 "Cyber Insurance Effective Date *",
#                 "Enter the date when the current cyber insurance policy became effective (when coverage started)."
#             ), unsafe_allow_html=True)
#             cyber_insurance_effective_date = st.date_input(
#                 "Effective Date", 
#                 key="cyber_insurance_effective_date",
#                 label_visibility="collapsed",
#                 help="Date the cyber insurance policy became effective"
#             )
#         else:
#             cyber_insurance_effective_date = None
    
#     # Important instruction for cyber insurance
#     if has_cyber_insurance == "Yes":
#         st.info("""
#         📋 **Important:** Please send a copy of your client's cyber insurance policy to support@seedpodcyber.com 
#         for review and verification as part of this audit process.
#         """)

#     # Loss History Section
#     st.markdown('<div class="loss-history"><h2>⚠️ Loss History</h2><p>Please indicate if your client organization has suffered from any of these losses in the last 3 years</p></div>', unsafe_allow_html=True)
    
#     loss_questions = [
#         ("extortion_claim", "Your client organization suffered an actual or attempted extortion demand that resulted in a claim"),
#         ("data_breach_claim", "Your client organization suffered an actual or attempted data breach that resulted in a claim"),
#         ("privacy_complaints", "Your client organization has experienced a claim or received complaints regarding privacy"),
#         ("copyright_infringement", "Your client organization performed copyright/trademark infringement that led to a claim"),
#         ("cybersecurity_circumstance", "You are aware of a circumstance involving cybersecurity, privacy or copyright/trademark infringement that may give rise to a claim"),
#         ("outage_4hours", "Your client organization suffered an outage that lasted longer than 4 hours")
#     ]
    
#     col_loss1, col_loss2 = st.columns(2)
#     loss_responses = {}
    
#     for i, (key, question) in enumerate(loss_questions):
#         with col_loss1 if i % 2 == 0 else col_loss2:
#             st.markdown(f"**{question}**")
#             loss_responses[key] = st.radio("Response", ["No", "Yes"], key=key, label_visibility="collapsed")
    
#     # Authentication Procedures
#     st.markdown('<div class="section-header"><h2>🔐 Authentication Procedures</h2></div>', unsafe_allow_html=True)
    
#     col_auth1, col_auth2 = st.columns(2)
    
#     with col_auth1:
#         st.markdown(create_tooltip(
#             "Employee Authentication of Customer Information Changes *",
#             "Is there a procedure where employees must authenticate all requested changes to customer information (bank accounts, routing numbers, etc.) by calling the vendor?"
#         ), unsafe_allow_html=True)
#         customer_info_auth = st.radio("Customer Info Authentication", ["No", "Yes"], key="customer_info_auth", label_visibility="collapsed")
    
#     with col_auth2:
#         st.markdown(create_tooltip(
#             "Wire Transfer Request Validation *",
#             "Is there a procedure to validate wire transfer requests made by Senior Executives/employees by calling the requestor or face-to-face communication?"
#         ), unsafe_allow_html=True)
#         wire_transfer_validation = st.radio("Wire Transfer Validation", ["No", "Yes"], key="wire_transfer_validation", label_visibility="collapsed")
    
#     # Security Tools Assessment
#     st.markdown('<div class="security-controls"><h2>🛠️ Security Tools in Use</h2><p>Please indicate the status of each security tool at the client organization</p></div>', unsafe_allow_html=True)
    
#     security_tools = [
#         ("Patch Management (CIS 7.3) *",
#                 "Automated patch management for operating systems and applications with testing and deployment procedures. Critical for maintaining security baselines and closing vulnerability windows across client environments."
#             ),
#         ("Multi-Factor Authentication - all remote and local admin (CIS 6.4, 6.5) *",
#                 "MFA required for all administrative access including remote connections and local admin accounts. Prevents credential-based attacks and unauthorized administrative access to client systems."
#             ),
#         ("Access Control / Strong Password Policy / Unassociated account removal (CIS 5.1, 5.2, 5.3) *",
#                 "Comprehensive access control including role-based permissions, strong password policies (complexity, length, expiration), and automatic removal of unused accounts. Fundamental for maintaining client system security."
#             ),
#         ("Secure Remote Access (CIS 13.5) *",
#                 "VPN or zero-trust remote access solutions with encryption and authentication. Ensures secure connections for remote work and prevents unauthorized network access."
#             ),
#         ("Next Gen AV / Endpoint Detection and Response (EDR) (CIS 10.1, 13.7) *",
#                 "Advanced endpoint protection including behavioral analysis, threat hunting, and automated response capabilities. Goes beyond traditional antivirus to detect and respond to sophisticated threats."
#             ),
#         ("Email Filtering (CIS 9.2, 9.3, 9.4) *",
#                 "Advanced email security including spam filtering, malware detection, phishing protection, and safe attachment handling. Critical for preventing email-based attacks."
#             ),
#         ("Backup (min 1 online, 1 offline) w/ testing (for on-prem and hybrid environments) (CIS 11.2, 11.4) *",
#                 "Comprehensive backup strategy with both online (readily accessible) and offline (air-gapped) backups, including regular restore testing to ensure backup integrity and recovery procedures."
#             ),
#         ("Encryption on endpoints and in transit (CIS 3.1, 3.11) *",
#                 "Data encryption for stored data on endpoints (full disk encryption) and data in transit (TLS/SSL for communications). Protects data confidentiality even if devices are lost or communications intercepted."
#             ),
#         ("Security Awareness Training with Phish Simulations (CIS 14.2) *",
#                 "Regular security awareness training for end users including simulated phishing exercises to test and improve human security behaviors. Critical for preventing social engineering attacks."
#             ),
#         ("SPF, DKIM, DMARC (CIS 9.5) *",
#                 "Email authentication protocols that prevent email spoofing and phishing attacks. SPF verifies sender IP addresses, DKIM validates message authenticity, and DMARC provides policy enforcement."
#             ),
#         ("Remote Desktop Protocol (RDP) and Server Message Block (SMB) ports are blocked (CIS 4.5) *",
#                 "Network-level blocking of high-risk protocols (RDP port 3389, SMB ports 445/139) from internet access. These protocols are commonly exploited attack vectors and should not be directly accessible from the internet."
#             ),

#     ]
    
#     # Create columns for security tools
#     num_cols = 2
#     cols = st.columns(num_cols)
#     security_responses = {}
    
#     for i, (key, tool_name) in enumerate(security_tools):
#         with cols[i % num_cols]:
#             st.markdown(f"**{tool_name}**")
#             security_responses[key] = st.radio("Status", ["Present", "Not Present", "Partially Present","Not Applicable"], key=key, label_visibility="collapsed")
    
    
#     # Backup Procedures
#     st.markdown("**Back-ups - The organization makes:** *(select one)*")
#     backup_frequency = st.radio("Backup Frequency", [
#         "No back-ups of critical Data and Computer Systems",
#         "Occasional and full back-ups of critical Data and Computer Systems",
#         "Regular, full and incremental backups of critical Data and Computer Systems"
#     ], key="backup_frequency")
    
#     if backup_frequency != "No back-ups of critical Data and Computer Systems":
#         st.markdown("**System Recovery Time:** *How quickly could systems be operational?*")
#         recovery_time = st.radio("Recovery Time", [
#             "within 24 hours",
#             "within 25-48 hours", 
#             "within 49-130 hours",
#             "more than 130 hours"
#         ], key="recovery_time")
#     else:
#         recovery_time = "N/A"
    
#     # Patching and Updates
#     st.markdown("**Patching & Updates - The organization has:** *(select one)*")
#     patching_procedure = st.radio("Patching Procedure", [
#         "Manual Updates",
#         "Automatic updates enabled",
#         "Automatic updates enabled with patch management verification procedure"
#     ], key="patching_procedure")
    
#     # Multi-Factor Authentication
#     st.markdown("**Multi-Factor Authentication (MFA) is enabled for:** *(check all that apply)*")
#     mfa_usage = {}
#     mfa_usage['admin_accounts'] = st.checkbox("Administrative accounts (domain admin and local admin)", key="mfa_admin")
#     mfa_usage['remote_access'] = st.checkbox("Remote access to network/on VPN", key="mfa_remote")
#     mfa_usage['email_access'] = st.checkbox("Email account access", key="mfa_email")
    
#     # Web and Email Filtering
#     st.markdown("**The organization has:** *(select one)*")
#     filtering_status = st.radio("Filtering Status", [
#         "Neither web nor email filtering enabled",
#         "Web or email (DKIM, DMARC, SPF) filtering enabled",
#         "Web and email (DKIM, DMARC, SPF) filtering enabled"
#     ], key="filtering_status")
    
#     # Encryption
#     st.markdown("**Encryption is:** *(select one)*")
#     encryption_status = st.radio("Encryption Status", [
#         "Not deployed",
#         "Deployed for Data at rest",
#         "Deployed for Data at rest and in transit"
#     ], key="encryption_status")
    
#     if encryption_status == "Not deployed":
#         encryption_explanation = st.text_area("Please explain why encryption is not deployed:", key="encryption_explanation")
#     else:
#         encryption_explanation = ""
    
#     # Data Disposal
#     st.markdown("**When Data and equipment is no longer needed, the organization:** *(select one)*")
#     data_disposal = st.radio("Data Disposal", [
#         "Has no policies or procedures pertaining to the destruction of Data or retirement of Hardware",
#         "Disposes of old computers/devices/media responsibly",
#         "Disposes Hardware/media responsibly in accordance with a written Data retention & destruction policy"
#     ], key="data_disposal")
    
#     # Submit Button
#     submitted = st.form_submit_button("Submit Client Audit", use_container_width=True)

# # Handle form submission
# if submitted:
#     # Check required fields
#     required_fields_validation = []
    
#     if not first_name or first_name.strip() == "":
#         required_fields_validation.append("First Name")
#     if not last_name or last_name.strip() == "":
#         required_fields_validation.append("Last Name")
#     if not email or email.strip() == "":
#         required_fields_validation.append("Email")
#     if not organization_name or organization_name.strip() == "":
#         required_fields_validation.append("Organization Name")
#     if not org_address or org_address.strip() == "":
#         required_fields_validation.append("Organization Address")
#     if not org_website or org_website.strip() == "":
#         required_fields_validation.append("Organization Website")
#     if not naics_code or naics_code.strip() == "":
#         required_fields_validation.append("NAICS Code")
#     if not year_established:
#         required_fields_validation.append("Year of Establishment")
#     if not total_employees:
#         required_fields_validation.append("Total Employees")
#     if not expected_revenue and expected_revenue != 0:
#         required_fields_validation.append("Expected Revenue")
#     if not msp_name or msp_name.strip() == "":
#         required_fields_validation.append("MSP Name")
#     if has_cyber_insurance == "Yes" and cyber_insurance_effective_date is None:
#         required_fields_validation.append("Cyber Insurance Effective Date")
    
#     if required_fields_validation:
#         st.error(f"❌ Please complete the following required fields: {', '.join(required_fields_validation)}")
#     else:
#         # Collect all form data
#         form_data = {
#             'form_submission_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#             'submission_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#             'first_name': first_name,
#             'last_name': last_name,
#             'email': email,
#             'organization_name': organization_name,
#             'org_address': org_address,
#             'org_website': org_website,
#             'naics_code': naics_code,
#             'naics_description': selected_naics if selected_naics else "",
#             'year_established': year_established,
#             'total_employees': total_employees,
#             'expected_revenue': expected_revenue,
#             'msp_name': msp_name,
#             'has_cyber_insurance': has_cyber_insurance,
#             'cyber_insurance_effective_date': cyber_insurance_effective_date.strftime('%Y-%m-%d') if cyber_insurance_effective_date else "",
#             'customer_info_auth': customer_info_auth,
#             'wire_transfer_validation': wire_transfer_validation,
#             'backup_frequency': backup_frequency,
#             'recovery_time': recovery_time,
#             'patching_procedure': patching_procedure,
#             'filtering_status': filtering_status,
#             'encryption_status': encryption_status,
#             'encryption_explanation': encryption_explanation,
#             'data_disposal': data_disposal
#         }
        
#         # Add loss history responses
#         form_data.update(loss_responses)
        
#         # Add security tools responses
#         form_data.update(security_responses)
        
#         # Add security policies
#         form_data.update(security_policies)
        
#         # Add MFA usage
#         form_data.update(mfa_usage)
        
#         # Store form data in session state
#         st.session_state.form_data = form_data
#         st.session_state.form_submitted = True
        
#         # Create DataFrame and CSV
#         df = pd.DataFrame([form_data])
        
#         # Generate CSV
#         csv_buffer = io.StringIO()
#         df.to_csv(csv_buffer, index=False)
#         csv_data = csv_buffer.getvalue()
        
#         filename = f"client_audit_{organization_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
#         # Store CSV data in session state
#         st.session_state.csv_data = csv_data
#         st.session_state.filename = filename
        
#         # Send email with CSV attachment
#         email_sent = send_assessment_email(csv_data, filename, "Client Insurability Audit", form_data)
        
#         if email_sent:
#             st.session_state.email_sent = True

# # Display results after form submission
# if st.session_state.get('form_submitted', False):
#     # Display success message
#     if st.session_state.get('email_sent', False):
#         st.success("✅ Client audit submitted successfully and sent to our team!")
#         st.info("📧 Your client audit has been automatically emailed to support@seedpodcyber.com for review.")
        
#         # Additional cyber insurance instruction
#         if st.session_state.form_data.get('has_cyber_insurance') == 'Yes':
#             st.warning("🛡️ **Don't forget:** Please send a copy of your client's cyber insurance policy to support@seedpodcyber.com")
#     else:
#         st.success("✅ Client audit submitted successfully!")
#         st.warning("⚠️ Automatic email delivery failed. Please download your audit and email it manually to support@seedpodcyber.com")
        
#         # Additional cyber insurance instruction
#         if st.session_state.form_data.get('has_cyber_insurance') == 'Yes':
#             st.warning("🛡️ **Don't forget:** Please send a copy of your client's cyber insurance policy to support@seedpodcyber.com")
    
#     # Download button
#     st.download_button(
#         label="📥 Download Client Audit Data (CSV)",
#         data=st.session_state.csv_data,
#         file_name=st.session_state.filename,
#         mime="text/csv",
#         use_container_width=True
#     )
    
#     # Display summary
#     with st.expander("📊 Client Audit Summary", expanded=True):
#         col_summary1, col_summary2, col_summary3 = st.columns(3)
#         form_data = st.session_state.form_data
        
#         with col_summary1:
#             st.metric("Client Organization", form_data['organization_name'])
#             st.metric("Contact", f"{form_data['first_name']} {form_data['last_name']}")
#             st.metric("Employees", f"{form_data['total_employees']:,}")
            
#         with col_summary2:
#             st.metric("Expected Revenue", format_currency(form_data['expected_revenue']))
#             st.metric("MSP", form_data['msp_name'])
#             st.metric("Year Established", form_data['year_established'])
        
#         with col_summary3:
#             # Count security tools in use
#             tools_yes = sum(1 for k, v in form_data.items() if k.endswith('_tools') or k in ['email_filtering', 'dns_filtering', 'backup_onsite', 'backup_offsite', 'cloud_hosting', 'next_gen_av', 'edr_tools', 'firewall', 'hardware_inventory', 'software_inventory', 'saas_inventory', 'mfa_tools', 'pam_tools', 'security_training', 'vulnerability_scanning', 'siem_tools', 'soc_mdr', 'email_tools'] and v == 'Yes')
#             st.metric("Security Tools (Yes)", tools_yes)
            
#             # Count policies in place
#             policies_count = sum(1 for k, v in form_data.items() if k in ['written_security_plan', 'incident_response_plan', 'ciso_designated'] and v == True)
#             st.metric("Security Policies", policies_count)
            
#             # Cyber insurance status
#             cyber_status = "✅ Yes" if form_data.get('has_cyber_insurance') == 'Yes' else "❌ No"
#             st.metric("Cyber Insurance", cyber_status)
    
#     # Instructions for next steps
#     next_steps_text = """
#     **Next Steps:**
    
#     1. ✅ **Download your client audit data** using the button above
#     2. 📊 **Review the audit summary** for key client security metrics
#     3. 📋 **Follow up on identified gaps** in client security posture
#     4. 🔒 **Recommend security improvements** based on audit findings
#     5. 📞 **Schedule consultation** with SeedPod Cyber if needed
#     """
    
#     if st.session_state.form_data.get('has_cyber_insurance') == 'Yes':
#         next_steps_text += "\n    6. 🛡️ **Send cyber insurance policy** to support@seedpodcyber.com"
    
#     next_steps_text += "\n\n    Thank you for completing the Client Insurability Audit!"
    
#     st.info(next_steps_text)
    
#     # Option to reset form
#     st.markdown("---")
#     if st.button("🔄 Start New Client Audit", key="reset_audit", use_container_width=True):
#         for key in list(st.session_state.keys()):
#             if key != 'access_granted':  # Keep access granted
#                 del st.session_state[key]
#         st.rerun()

# # Copyright Footer
# st.markdown("---")
# st.markdown("""
# <div style="text-align: center; padding: 1rem; color: #666; font-size: 0.9em;">
#     Copyright 2025 SeedPod Cyber LLC, All Rights Reserved
# </div>
# """, unsafe_allow_html=True)


