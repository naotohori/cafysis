class DT13(object):
    # U_BL
    BL_PS = 23.0
    BL_SB = 10.0
    BL_SP = 64.0

    # U_BA
    BA_PSB =  5.0
    BA_PSP = 20.0
    BA_BSP =  5.0
    BA_SPS = 20.0
    
    # U_EV
    #exv_dist = 3.2
    #exv_coef = 1.0
    #n_sep_nlocal_P = 3
    #n_sep_nlocal_S = 3
    #n_sep_nlocal_B = 2
    
    # U_ST
    ST_DIST = 1.4
    ST_DIH = 4.0
    ST_U0 = {
        #         h       s      Tm
        'AA':  (4.348, -0.319,  298.9),
        'AC':  (4.311, -0.319,  298.9),
        'AG':  (5.116,  5.301,  341.2),
        'AU':  (4.311, -0.319,  298.9),
        'CA':  (4.287, -0.319,  298.9),
        'CC':  (4.015, -1.567,  285.8),
        'CG':  (4.602,  0.774,  315.5),
        'CU':  (3.995, -1.567,  285.8),
        'GA':  (5.079,  5.301,  341.2),
        'GC':  (5.075,  4.370,  343.2),
        'GG':  (5.555,  7.346,  366.3),
        'GU':  (4.977,  2.924,  338.2),
        'UA':  (4.287, -0.319,  298.9),
        'UC':  (3.992, -1.567,  285.8),
        'UG':  (5.032,  2.924,  338.2),
        'UU':  (3.370, -3.563,  251.6),
    }
    
    # U_HB
    HB_DIST = 5.0
    HB_ANGL = 1.5
    HB_DIH_HBOND = 0.15
    HB_DIH_CHAIN = 0.15
    HB_U0 = -2.434

    # U_EV
    n_sep_nlocal_P = 3
    n_sep_nlocal_S = 3
    n_sep_nlocal_B = 2
