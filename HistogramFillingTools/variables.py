from calculation import Calculation, CalculationDataMC, WeightCalculation
import numpy as np
from math import pi

'''
******************************************************************************
*Tree    :MuonMomentumCalibrationTree: MuonMomentumCalibrationTree                            *
*Entries : 44547438 : Total =     23707704675 bytes  File  Size = 15925253674 *
*        :          : Tree compression factor =   1.49                       *
******************************************************************************
*Br    0 :RunNumber : RunNumber/i                                            *
*Entries : 44547438 : Total  Size=  178960836 bytes  File Size  =    1759927 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression= 101.61     *
*............................................................................*
*Br    1 :LumiBlock : LumiBlock/i                                            *
*Entries : 44547438 : Total  Size=  178960836 bytes  File Size  =    5058212 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=  35.35     *
*............................................................................*
*Br    2 :ChannelNumber : ChannelNumber/i                                    *
*Entries : 44547438 : Total  Size=  178986760 bytes  File Size  =    1653629 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression= 108.16     *
*............................................................................*
*Br    3 :EvtNumber : EvtNumber/l                                            *
*Entries : 44547438 : Total  Size=  357597917 bytes  File Size  =  184931089 *
*Baskets :    10236 : Basket Size=      32000 bytes  Compression=   1.93     *
*............................................................................*
*Br    4 :EventWeight : EventWeight/F                                        *
*Entries : 44547438 : Total  Size=  178973798 bytes  File Size  =    1763054 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression= 101.44     *
*............................................................................*
*Br    5 :Pair_CB_Pt : Pair_CB_Pt/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  161031015 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.11     *
*............................................................................*
*Br    6 :Pair_CB_Eta : Pair_CB_Eta/F                                        *
*Entries : 44547438 : Total  Size=  178973798 bytes  File Size  =  165486416 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br    7 :Pair_CB_Phi : Pair_CB_Phi/F                                        *
*Entries : 44547438 : Total  Size=  178973798 bytes  File Size  =  165902440 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br    8 :Pair_CB_Mass : Pair_CB_Mass/F                                      *
*Entries : 44547438 : Total  Size=  178980279 bytes  File Size  =  155368679 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.15     *
*............................................................................*
*Br    9 :Pair_ID_Mass : Pair_ID_Mass/F                                      *
*Entries : 44547438 : Total  Size=  178980279 bytes  File Size  =  156024030 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.15     *
*............................................................................*
*Br   10 :Pair_ME_Mass : Pair_ME_Mass/F                                      *
*Entries : 44547438 : Total  Size=  178980279 bytes  File Size  =  156702996 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.14     *
*............................................................................*
*Br   11 :Pair_MSOE_Mass : Pair_MSOE_Mass/F                                  *
*Entries : 44547438 : Total  Size=  178993241 bytes  File Size  =  157263727 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.14     *
*............................................................................*
*Br   12 :Pos_CB_Pt : Pos_CB_Pt/F                                            *
*Entries : 44547438 : Total  Size=  178960836 bytes  File Size  =  159403921 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.12     *
*............................................................................*
*Br   13 :Pos_CB_CalibPt : Pos_CB_CalibPt/F                                  *
*Entries : 44547438 : Total  Size=  178993241 bytes  File Size  =  159468447 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.12     *
*............................................................................*
*Br   14 :Pos_CB_Eta : Pos_CB_Eta/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  165418229 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   15 :Pos_CB_Phi : Pos_CB_Phi/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  165853924 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   16 :Pos_CB_TrackPars : vector<float>                                   *
*Entries : 44547438 : Total  Size= 1520127077 bytes  File Size  = 1003478110 *
*Baskets :    41148 : Basket Size=      32000 bytes  Compression=   1.51     *
*............................................................................*
*Br   17 :Pos_CB_TrackCovMatrix : vector<float>                              *
*Entries :44547438 : Total  Size= 3307950902 bytes  File Size  = 2791418124 *
*Baskets :    82303 : Basket Size=      32000 bytes  Compression=   1.18     *
*............................................................................*
*Br   18 :Pos_ID_Pt : Pos_ID_Pt/F                                            *
*Entries : 44547438 : Total  Size=  178960836 bytes  File Size  =  159467073 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.12     *
*............................................................................*
*Br   19 :Pos_ID_CalibPt : Pos_ID_CalibPt/F                                  *
*Entries : 44547438 : Total  Size=  178993241 bytes  File Size  =  159627850 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.12     *
*............................................................................*
*Br   20 :Pos_ID_Eta : Pos_ID_Eta/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  165420534 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   21 :Pos_ID_Phi : Pos_ID_Phi/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  165853586 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   22 :Pos_MS_Pt : Pos_MS_Pt/F                                            *
*Entries : 44547438 : Total  Size=  178960836 bytes  File Size  =  161360883 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.11     *
*............................................................................*
*Br   23 :Pos_MS_CalibPt : Pos_MS_CalibPt/F                                  *
*Entries : 44547438 : Total  Size=  178993241 bytes  File Size  =    2706928 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=  66.08     *
*............................................................................*
*Br   24 :Pos_MS_Eta : Pos_MS_Eta/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  165131358 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   25 :Pos_MS_Phi : Pos_MS_Phi/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  165635365 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   26 :Pos_ME_Pt : Pos_ME_Pt/F                                            *
*Entries : 44547438 : Total  Size=  178960836 bytes  File Size  =  159560621 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.12     *
*............................................................................*
*Br   27 :Pos_ME_CalibPt : Pos_ME_CalibPt/F                                  *
*Entries : 44547438 : Total  Size=  178993241 bytes  File Size  =    2155911 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=  82.96     *
*............................................................................*
*Br   28 :Pos_ME_Eta : Pos_ME_Eta/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  165347022 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   29 :Pos_ME_Phi : Pos_ME_Phi/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  165784800 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   30 :Pos_MSOE_Pt : Pos_MSOE_Pt/F                                        *
*Entries : 44547438 : Total  Size=  178973798 bytes  File Size  =  159254904 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.12     *
*............................................................................*
*Br   31 :Pos_MSOE_CalibPt : Pos_MSOE_CalibPt/F                              *
*Entries : 44547438 : Total  Size=  179006203 bytes  File Size  =    3250080 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=  55.04     *
*............................................................................*
*Br   32 :Pos_MSOE_Eta : Pos_MSOE_Eta/F                                      *
*Entries : 44547438 : Total  Size=  178980279 bytes  File Size  =  164949315 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   33 :Pos_MSOE_Phi : Pos_MSOE_Phi/F                                      *
*Entries : 44547438 : Total  Size=  178980279 bytes  File Size  =  165447266 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   34 :Pos_d0Significance : Pos_d0Significance/F                          *
*Entries : 44547438 : Total  Size=  179019165 bytes  File Size  =  166312553 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   35 :Pos_neflowisol20 : Pos_neflowisol20/F                              *
*Entries : 44547438 : Total  Size=  179006203 bytes  File Size  =  163684914 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.09     *
*............................................................................*
*Br   36 :Pos_topoetcone20 : Pos_topoetcone20/F                              *
*Entries : 44547438 : Total  Size=  179006203 bytes  File Size  =  165655555 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   37 :Pos_ptcone20_TightTTVA_pt500 : Pos_ptcone20_TightTTVA_pt500/F      *
*Entries : 44547438 : Total  Size=  179084389 bytes  File Size  =   61227064 *
*Baskets :     6480 : Basket Size=      32000 bytes  Compression=   2.92     *
*............................................................................*
*Br   38 :Pos_ptvarcone30_TightTTVA_pt500 : Pos_ptvarcone30_TightTTVA_pt500/F*
*Entries : 44547438 : Total  Size=  179103841 bytes  File Size  =   82199614 *
*Baskets :     6480 : Basket Size=      32000 bytes  Compression=   2.18     *
*............................................................................*
*Br   39 :Pos_ptvarcone30_TightTTVA_pt1000 :                                 *
*         | Pos_ptvarcone30_TightTTVA_pt1000/F                               *
*Entries : 44547438 : Total  Size=  179110325 bytes  File Size  =   62503012 *
*Baskets :     6480 : Basket Size=      32000 bytes  Compression=   2.86     *
*............................................................................*
*Br   40 :Pos_Quality : Pos_Quality/I                                        *
*Entries : 44547438 : Total  Size=  178973798 bytes  File Size  =    9357132 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=  19.11     *
*............................................................................*
*Br   41 :Pos_TruthPt : Pos_TruthPt/F                                        *
*Entries : 44547438 : Total  Size=  178973798 bytes  File Size  =    1640675 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression= 109.01     *
*............................................................................*
*Br   42 :Pos_TruthEta : Pos_TruthEta/F                                      *
*Entries : 44547438 : Total  Size=  178980279 bytes  File Size  =    1647152 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression= 108.58     *
*............................................................................*
*Br   43 :Pos_TruthPhi : Pos_TruthPhi/F                                      *
*Entries : 44547438 : Total  Size=  178980279 bytes  File Size  =    1647152 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression= 108.58     *
*............................................................................*
*Br   44 :Pos_IsCBMuon : Pos_IsCBMuon/O                                      *
*Entries : 44547438 : Total  Size=   45039547 bytes  File Size  =    1622776 *
*Baskets :     4031 : Basket Size=      32000 bytes  Compression=  27.70     *
*............................................................................*
*Br   45 :Neg_CB_Pt : Neg_CB_Pt/F                                            *
*Entries : 44547438 : Total  Size=  178960836 bytes  File Size  =  159410279 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.12     *
*............................................................................*
*Br   46 :Neg_CB_CalibPt : Neg_CB_CalibPt/F                                  *
*Entries : 44547438 : Total  Size=  178993241 bytes  File Size  =  159474918 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.12     *
*............................................................................*
*Br   47 :Neg_CB_Eta : Neg_CB_Eta/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  165416181 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   48 :Neg_CB_Phi : Neg_CB_Phi/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  165850384 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   49 :Neg_CB_TrackPars : vector<float>                                   *
*Entries : 44547438 : Total  Size= 1520127077 bytes  File Size  = 1003824024 *
*Baskets :    41148 : Basket Size=      32000 bytes  Compression=   1.51     *
*............................................................................*
*Br   50 :Neg_CB_TrackCovMatrix : vector<float>                              *
*Entries :44547438 : Total  Size= 3307950902 bytes  File Size  = 2791332503 *
*Baskets :    82303 : Basket Size=      32000 bytes  Compression=   1.18     *
*............................................................................*
*Br   51 :Neg_ID_Pt : Neg_ID_Pt/F                                            *
*Entries : 44547438 : Total  Size=  178960836 bytes  File Size  =  159476265 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.12     *
*............................................................................*
*Br   52 :Neg_ID_CalibPt : Neg_ID_CalibPt/F                                  *
*Entries : 44547438 : Total  Size=  178993241 bytes  File Size  =  159638604 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.12     *
*............................................................................*
*Br   53 :Neg_ID_Eta : Neg_ID_Eta/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  165416355 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   54 :Neg_ID_Phi : Neg_ID_Phi/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  165850176 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   55 :Neg_MS_Pt : Neg_MS_Pt/F                                            *
*Entries : 44547438 : Total  Size=  178960836 bytes  File Size  =  161370819 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.11     *
*............................................................................*
*Br   56 :Neg_MS_CalibPt : Neg_MS_CalibPt/F                                  *
*Entries : 44547438 : Total  Size=  178993241 bytes  File Size  =    2693318 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=  66.41     *
*............................................................................*
*Br   57 :Neg_MS_Eta : Neg_MS_Eta/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  165140086 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   58 :Neg_MS_Phi : Neg_MS_Phi/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  165639130 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   59 :Neg_ME_Pt : Neg_ME_Pt/F                                            *
*Entries : 44547438 : Total  Size=  178960836 bytes  File Size  =  159572469 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.12     *
*............................................................................*
*Br   60 :Neg_ME_CalibPt : Neg_ME_CalibPt/F                                  *
*Entries : 44547438 : Total  Size=  178993241 bytes  File Size  =    2095873 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=  85.34     *
*............................................................................*
*Br   61 :Neg_ME_Eta : Neg_ME_Eta/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  165357277 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   62 :Neg_ME_Phi : Neg_ME_Phi/F                                          *
*Entries : 44547438 : Total  Size=  178967317 bytes  File Size  =  165795008 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   63 :Neg_MSOE_Pt : Neg_MSOE_Pt/F                                        *
*Entries : 44547438 : Total  Size=  178973798 bytes  File Size  =  159276223 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.12     *
*............................................................................*
*Br   64 :Neg_MSOE_CalibPt : Neg_MSOE_CalibPt/F                              *
*Entries : 44547438 : Total  Size=  179006203 bytes  File Size  =    3196922 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=  55.95     *
*............................................................................*
*Br   65 :Neg_MSOE_Eta : Neg_MSOE_Eta/F                                      *
*Entries : 44547438 : Total  Size=  178980279 bytes  File Size  =  164970969 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   66 :Neg_MSOE_Phi : Neg_MSOE_Phi/F                                      *
*Entries : 44547438 : Total  Size=  178980279 bytes  File Size  =  165471122 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   67 :Neg_d0Significance : Neg_d0Significance/F                          *
*Entries : 44547438 : Total  Size=  179019165 bytes  File Size  =  166300759 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.08     *
*............................................................................*
*Br   68 :Neg_z0SinTheta : Neg_z0SinTheta/F                                  *
*Entries : 44547438 : Total  Size=  178993241 bytes  File Size  =  163170169 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.10     *
*............................................................................*
*Br   69 :Neg_neflowisol20 : Neg_neflowisol20/F                              *
*Entries : 44547438 : Total  Size=  179006203 bytes  File Size  =  163654094 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression=   1.09     *
*............................................................................*
*Br   70 :Neg_ptcone20_TightTTVA_pt500 : Neg_ptcone20_TightTTVA_pt500/F      *
*Entries : 44547438 : Total  Size=  179084389 bytes  File Size  =   61233129 *
*Baskets :     6480 : Basket Size=      32000 bytes  Compression=   2.92     *
*............................................................................*
*Br   71 :Neg_ptvarcone30_TightTTVA_pt500 : Neg_ptvarcone30_TightTTVA_pt500/F*
*Entries : 44547438 : Total  Size=  179103841 bytes  File Size  =   82330634 *
*Baskets :     6480 : Basket Size=      32000 bytes  Compression=   2.17     *
*............................................................................*
*Br   72 :Neg_ptvarcone30_TightTTVA_pt1000 :                                 *
*         | Neg_ptvarcone30_TightTTVA_pt1000/F                               *
*Entries : 44547438 : Total  Size=  179110325 bytes  File Size  =   62576945 *
*Baskets :     6480 : Basket Size=      32000 bytes  Compression=   2.86     *
*............................................................................*
*Br   73 :Neg_TruthPt : Neg_TruthPt/F                                        *
*Entries : 44547438 : Total  Size=  178973798 bytes  File Size  =    1640675 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression= 109.01     *
*............................................................................*
*Br   74 :Neg_TruthEta : Neg_TruthEta/F                                      *
*Entries : 44547438 : Total  Size=  178980279 bytes  File Size  =    1647152 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression= 108.58     *
*............................................................................*
*Br   75 :Neg_TruthPhi : Neg_TruthPhi/F                                      *
*Entries : 44547438 : Total  Size=  178980279 bytes  File Size  =    1647152 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression= 108.58     *
*............................................................................*
*Br   76 :Neg_IsCBMuon : Neg_IsCBMuon/O                                      *
*Entries : 44547438 : Total  Size=   45039547 bytes  File Size  =    1661042 *
*Baskets :     4031 : Basket Size=      32000 bytes  Compression=  27.07     *
*............................................................................*
*Br   77 :PileupWeight : PileupWeight/F                                      *
*Entries : 44547438 : Total  Size=  178980279 bytes  File Size  =    1769531 *
*Baskets :     6477 : Basket Size=      32000 bytes  Compression= 101.07     *
*............................................................................*
*Br   78 :TotalWeight : TotalWeight/F                                        *
*Entries : 44547438 : Total  Size=  179138842 bytes  File Size  =    1953052 *
*Baskets :     7841 : Basket Size=      32000 bytes  Compression=  91.64     *
*............................................................................*
*Br   79 :SampleWeight : SampleWeight/F                                      *
*Entries : 44547438 : Total  Size=  179146687 bytes  File Size  =    1960893 *
*Baskets :     7841 : Basket Size=      32000 bytes  Compression=  91.28     *
*............................................................................*
*Br   80 :ResoIndex : ResoIndex/I                                            *
*Entries : 44547438 : Total  Size=  179123152 bytes  File Size  =   19558868 *
*Baskets :     7841 : Basket Size=      32000 bytes  Compression=   9.15     *
*............................................................................*
*Br   81 :PeriodIndex : PeriodIndex/I                                        *
*Entries : 44547438 : Total  Size=  179138842 bytes  File Size  =    1937492 *
*Baskets :     7841 : Basket Size=      32000 bytes  Compression=  92.38     *
*............................................................................*
*Br   82 :SampleType : SampleType/I                                          *
*Entries : 44547438 : Total  Size=  179130997 bytes  File Size  =    1815344 *
*Baskets :     7841 : Basket Size=      32000 bytes  Compression=  98.59     *
*............................................................................*
'''

def weight(event, isData):
    return event["TotalWeight"]
branches = ["TotalWeight"]
calc_weight = WeightCalculation(weight, branches)
