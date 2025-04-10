
def calc_top_bottom_discount_rate(df_spread, spreadChoice, ovRating, cLength, s1Yr, s2Yr, s3Yr, s5Yr, s7Yr, s10Yr, discCorpContract):
    
    # Filter df_spread by spreadChoice and ovRating then use cLength to determine the discount rate
    
    if cLength == 1 or cLength == 2 or cLength == 3 or cLength == 5 or cLength == 7 or cLength == 10:
        pass   
    