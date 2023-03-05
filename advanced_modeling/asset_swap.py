from QuantLib import *
import unittest

#class AssetSwapTest(unittest.TestCase):
#    def setUp(self):
# initial setup
termStructure = RelinkableYieldTermStructureHandle()
swapSettlementDays = 2
faceAmount = 100.0
fixedConvention = Unadjusted
compounding = Continuous
fixedFrequency = Annual
floatingFrequency = Semiannual
iborIndex = Euribor(Period(floatingFrequency), termStructure)
calendar = iborIndex.fixingCalendar()
swapIndex =  SwapIndex("EuriborSwapIsdaFixA", Period(10,Years), swapSettlementDays,
                            iborIndex.currency(), calendar,
                            Period(fixedFrequency), fixedConvention,
                            iborIndex.dayCounter(), iborIndex)
spread = 0.0
nonnullspread = 0.003
#today = Date(24, April, 2007)
today = Date(4, March, 2023)
Settings.instance().evaluationDate = today
termStructure.linkTo(FlatForward(today, 0.05, Actual365Fixed()))
yieldCurve = FlatForward(today, 0.05, Actual365Fixed())
pricer = BlackIborCouponPricer()
swaptionVolatilityStructure = SwaptionVolatilityStructureHandle(ConstantSwaptionVolatility(today, NullCalendar(),Following, 0.2, Actual365Fixed()))
meanReversionQuote = QuoteHandle(SimpleQuote(0.01))
cmspricer = AnalyticHaganPricer(swaptionVolatilityStructure,
                                GFunctionFactory.Standard,
                                meanReversionQuote)

def mytest():
    bondCalendar = TARGET()
    settlementDays = 3

    ## Fixed Underlying bond (Isin: DE0001135275 DBR 4 01/04/37)
    ## maturity doesn't occur on a business day
    
    bondSchedule = Schedule(Date(4, March, 2023),
                            Date(4, March, 2028),
                            Period(Annual), bondCalendar,
                            Unadjusted, Unadjusted,
                            DateGeneration.Backward, False)
    faceAmount = 100.00
    bond = FixedRateBond(settlementDays, faceAmount,
                         bondSchedule,[0.04],
                         ActualActual(ActualActual.ISDA),
                         Following,
                         100.0, Date(4, March, 2023))

    #print (dir(bond))
    #for cf in bond.cashflows():
    #    print (cf.date(), cf.amount())

    #print (dir(termStructure))
    #print (help(termStructure))
    #for d in bondSchedule.dates():
    #    print (termStructure.discount(d))
    
    #print (termStructure.discount(Date(5, January, 2037)))
    #print (termStructure.forwardRate(Date(5, January, 2036), Date(5, January, 2037),
    #                                 ActualActual(ActualActual.ISDA), Continuous))
    bondEngine = DiscountingBondEngine(termStructure)
    ##swapEngine = DiscountingSwapEngine(self.termStructure, False)
    bond.setPricingEngine(bondEngine)
    #
    print (bond.cleanPrice())
    print (bond.dirtyPrice())
    payFixedRate = True
    bondPrice = 90.00
    isPar = True
    parAssetSwap = AssetSwap(payFixedRate,
                             bond, bondPrice,
                             iborIndex, spread,
                             Schedule(),
                             iborIndex.dayCounter(),
                             isPar)

    swapEngine =  DiscountingSwapEngine(termStructure, True,
                                        bond.settlementDate(),
                                        Settings.instance().evaluationDate)

    parAssetSwap.setPricingEngine(swapEngine)
    print(dir(parAssetSwap))
    fairCleanPrice = parAssetSwap.fairCleanPrice()
    fairSpread = parAssetSwap.fairSpread()
    print(parAssetSwap.legNPV(1))
    print(parAssetSwap.legNPV(0))
    for cf in list(parAssetSwap.leg(1)):
        print (cf.date(), cf.amount())
    for cf in list(parAssetSwap.leg(0)):
        print (cf.date(), cf.amount())
    print (fairCleanPrice)
    print (parAssetSwap.NPV())
    print (fairSpread)



def testConsistency():
    """Testing consistency between fair price and fair spread..."""
    bondCalendar = TARGET()
    settlementDays = 3

    ## Fixed Underlying bond (Isin: DE0001135275 DBR 4 01/04/37)
    ## maturity doesn't occur on a business day
    
    bondSchedule = Schedule(Date(4,January,2005),
                            Date(4,January,2037),
                            Period(Annual), bondCalendar,
                            Unadjusted, Unadjusted,
                            DateGeneration.Backward, False)
    bond = FixedRateBond(settlementDays, faceAmount,
                         bondSchedule,[0.04],
                         ActualActual(ActualActual.ISDA),
                         Following,
                         100.0, Date(4,January,2005))

    #print (dir(bond))
    for cf in bond.cashflows():
        print (cf.date(), cf.amount())

    #print (dir(termStructure))
    #print (help(termStructure))
    print (termStructure.discount(Date(5, January, 2037)))
    print (termStructure.forwardRate(Date(5, January, 2036), Date(5, January, 2037),
                                     ActualActual(ActualActual.ISDA), Continuous))
    bondEngine = DiscountingBondEngine(termStructure)
    #swapEngine = DiscountingSwapEngine(self.termStructure, False)
    bond.setPricingEngine(bondEngine)
    
    print (bond.cleanPrice())
    print (bond.dirtyPrice())
    payFixedRate = True
    bondPrice = 95.00
    isPar = True
    parAssetSwap = AssetSwap(payFixedRate,
                             bond, bondPrice,
                             iborIndex, spread,
                             Schedule(),
                             iborIndex.dayCounter(),
                             isPar)

    swapEngine =  DiscountingSwapEngine(termStructure, True,
                                        bond.settlementDate(),
                                        Settings.instance().evaluationDate)

    parAssetSwap.setPricingEngine(swapEngine)
    print(dir(parAssetSwap))
    fairCleanPrice = parAssetSwap.fairCleanPrice()
    fairSpread = parAssetSwap.fairSpread()
    #print(parAssetSwap.legNPV(1))
    #print(parAssetSwap.legNPV(0))
    for cf in list(parAssetSwap.leg(1)):
        print (cf.date(), cf.amount())
    print (fairCleanPrice)
    print (fairSpread)
    import sys
    sys.exit()

#        tolerance = 1.0e-13
#   
#        assetSwap2 = AssetSwap(payFixedRate, bond, fairCleanPrice,
#                             self.iborIndex, self.spread,
#                             Schedule(),
#                             self.iborIndex.dayCounter(),
#                             isPar)
#        
#        assetSwap2.setPricingEngine(swapEngine)
#        self.assertFalse(abs(assetSwap2.NPV())>tolerance,
#        "\npar asset swap fair clean price doesn't zero the NPV: "
#        + "\n  clean price:      " + str(bondPrice)
#        + "\n  fair clean price: " + str(fairCleanPrice)
#        + "\n  NPV:              " + str(assetSwap2.NPV())
#        + "\n  tolerance:        " + str(tolerance))
#    
#        self.assertFalse(abs(assetSwap2.fairCleanPrice() - fairCleanPrice)>tolerance,
#        "\npar asset swap fair clean price doesn't equal input "
#        + "clean price at zero NPV: "
#        + "\n  input clean price: " + str(fairCleanPrice)
#        + "\n  fair clean price:  " + str(assetSwap2.fairCleanPrice())
#        + "\n  NPV:               " + str(assetSwap2.NPV())
#        + "\n  tolerance:         " + str(tolerance))
#    
#        self.assertFalse(abs(assetSwap2.fairSpread() - self.spread)>tolerance,
#        "\npar asset swap fair spread doesn't equal input spread "
#        + "at zero NPV: " 
#        + "\n  input spread: " + str(self.spread )
#        + "\n  fair spread:  " + str(assetSwap2.fairSpread() )
#        + "\n  NPV:          " + str(assetSwap2.NPV() )
#        + "\n  tolerance:    " + str(tolerance))
#
#        assetSwap3 = AssetSwap(payFixedRate,
#                             bond, bondPrice,
#                             self.iborIndex, fairSpread,
#                             Schedule(),
#                             self.iborIndex.dayCounter(),
#                             isPar)
#        assetSwap3.setPricingEngine(swapEngine)
#        self.assertFalse(abs(assetSwap3.NPV())>tolerance,
#        "\npar asset swap fair spread doesn't zero the NPV: "
#        + "\n  spread:      " + str(self.spread)
#        + "\n  fair spread: " + str(fairSpread)
#        + "\n  NPV:         " + str(assetSwap3.NPV())
#        + "\n  tolerance:   " + str(tolerance))
#        
#        self.assertFalse(abs(assetSwap3.fairCleanPrice() - bondPrice)>tolerance,
#        "\npar asset swap fair clean price doesn't equal input "
#        + "clean price at zero NPV: "
#        + "\n  input clean price: " + str(bondPrice)
#        + "\n  fair clean price:  " + str(assetSwap3.fairCleanPrice())
#        + "\n  NPV:               " + str(assetSwap3.NPV())
#        + "\n  tolerance:         " + str(tolerance))
#    
#        self.assertFalse(abs(assetSwap3.fairSpread() - fairSpread)>tolerance,
#        "\npar asset swap fair spread doesn't equal input spread at"
#        + " zero NPV: "
#        + "\n  input spread: " + str(fairSpread)
#        + "\n  fair spread:  " + str(assetSwap3.fairSpread())
#        + "\n  NPV:          " + str(assetSwap3.NPV())
#        + "\n  tolerance:    " + str(tolerance))
#    
#
#        ## let's change the npv date
#        swapEngine = DiscountingSwapEngine(self.termStructure,
#                              True,
#                              bond.settlementDate(),
#                              bond.settlementDate())
#
#        parAssetSwap.setPricingEngine(swapEngine)
#        ## fair clean price and fair spread should not change
#        self.assertFalse(abs(parAssetSwap.fairCleanPrice() - fairCleanPrice)>tolerance,
#            "\npar asset swap fair clean price changed with NpvDate:"
#            + "\n expected clean price: " + str(fairCleanPrice)
#            + "\n fair clean price:     " + str(parAssetSwap.fairCleanPrice())
#            + "\n tolerance:            " + str(tolerance))
#    
#        self.assertFalse(abs(parAssetSwap.fairSpread() - fairSpread)>tolerance, 
#            "\npar asset swap fair spread changed with NpvDate:"
#            + "\n  expected spread: " + str(fairSpread)
#            + "\n  fair spread:     " + str(parAssetSwap.fairSpread())
#            + "\n  tolerance:       " + str(tolerance))
#    
#        assetSwap2 = AssetSwap(payFixedRate,    
#                           bond, fairCleanPrice,
#                           self.iborIndex, self.spread,
#                           Schedule(),
#                           self.iborIndex.dayCounter(),
#                           isPar)
#        assetSwap2.setPricingEngine(swapEngine)
#        self.assertFalse(abs(assetSwap2.NPV())>tolerance, 
#            "\npar asset swap fair clean price doesn't zero the NPV: "
#            + "\n  clean price:      " + str(bondPrice)
#            + "\n  fair clean price: " + str(fairCleanPrice)
#            + "\n  NPV:              " + str(assetSwap2.NPV())
#            + "\n  tolerance:        " + str(tolerance))
#    
#        self.assertFalse(abs(assetSwap2.fairCleanPrice() - fairCleanPrice)>tolerance,
#            "\npar asset swap fair clean price doesn't equal input "
#            + "clean price at zero NPV: "
#            + "\n  input clean price: " + str(fairCleanPrice)
#            + "\n  fair clean price:  " + str(assetSwap2.fairCleanPrice())
#            + "\n  NPV:               " + str(assetSwap2.NPV())
#            + "\n  tolerance:         " + str(tolerance))
#    
#        self.assertFalse(abs(assetSwap2.fairSpread() - self.spread)>tolerance,
#            "\npar asset swap fair spread doesn't equal input spread at zero NPV: "
#            + "\n  input spread: " + str(self.spread)
#            + "\n  fair spread:  " + str(assetSwap2.fairSpread())
#            + "\n  NPV:          " + str(assetSwap2.NPV())
#            + "\n  tolerance:    " + str(tolerance))
#
#        assetSwap3 = AssetSwap(payFixedRate,
#                           bond, bondPrice,
#                           self.iborIndex, fairSpread,
#                           Schedule(),
#                           self.iborIndex.dayCounter(),
#                           isPar)
#        assetSwap3.setPricingEngine(swapEngine)
#        self.assertFalse(abs(assetSwap3.NPV())>tolerance, 
#            "\npar asset swap fair spread doesn't zero the NPV: "
#            + "\n  spread:      " + str(self.spread)
#            + "\n  fair spread: " + str(fairSpread)
#            + "\n  NPV:         " + str(assetSwap3.NPV())
#            + "\n  tolerance:   " + str(tolerance))
#    
#        self.assertFalse(abs(assetSwap3.fairCleanPrice() - bondPrice)>tolerance,
#            "\npar asset swap fair clean price doesn't equal input "
#            + "clean price at zero NPV: "
#            + "\n  input clean price: " + str(bondPrice)
#            + "\n  fair clean price:  " + str(assetSwap3.fairCleanPrice())
#            + "\n  NPV:               " + str(assetSwap3.NPV())
#            + "\n  tolerance:         " + str(tolerance))
#    
#        self.assertFalse(abs(assetSwap3.fairSpread() - fairSpread)>tolerance,
#            "\npar asset swap fair spread doesn't equal input spread at zero NPV: "
#            + "\n  input spread: " + str(fairSpread)
#            + "\n  fair spread:  " + str(assetSwap3.fairSpread())
#            + "\n  NPV:          " + str(assetSwap3.NPV())
#            + "\n  tolerance:    " + str(tolerance))
#    

#
#    def testImpliedValue(self):
#        """Testing implied bond value against asset-swap fair price with null spread..."""
#        bondCalendar = TARGET()
#        settlementDays = 3
#        fixingDays = 2
#        payFixedRate = True
#        parAssetSwap = True
#        inArrears = False
#
#        ## Fixed Underlying bond (Isin: DE0001135275 DBR 4 01/04/37)
#        ## maturity doesn't occur on a business day
#
#        fixedBondSchedule1 = Schedule(Date(4,January,2005),
#                                    Date(4,January,2037),
#                                    Period(Annual), bondCalendar,
#                                    Unadjusted, Unadjusted,
#                                    DateGeneration.Backward, False)
#        fixedBond1 = FixedRateBond(settlementDays, self.faceAmount,
#                                               fixedBondSchedule1,
#                                               [0.04],
#                                               ActualActual(ActualActual.ISDA),
#                                               Following,
#                                               100.0, Date(4,January,2005))
#
#        bondEngine = DiscountingBondEngine(self.termStructure)
#        swapEngine = DiscountingSwapEngine(self.termStructure, False)
#        fixedBond1.setPricingEngine(bondEngine)
#
#        fixedBondPrice1 = fixedBond1.cleanPrice()
#        fixedBondAssetSwap1 = AssetSwap(payFixedRate,
#                                      fixedBond1, fixedBondPrice1,
#                                      self.iborIndex, self.spread,
#                                      Schedule(),
#                                      self.iborIndex.dayCounter(),
#                                      parAssetSwap)
#        fixedBondAssetSwap1.setPricingEngine(swapEngine)
#        fixedBondAssetSwapPrice1 = fixedBondAssetSwap1.fairCleanPrice()
#        tolerance = 1.0e-13
#        
#        error1 = abs(fixedBondAssetSwapPrice1-fixedBondPrice1)
#
#        self.assertFalse(error1>tolerance, 
#            "wrong zero spread asset swap price for fixed bond:"
#            + "\n  bond's clean price:    " + str(fixedBondPrice1)
#            + "\n  asset swap fair price: " + str(fixedBondAssetSwapPrice1)
#            + "\n  error:                 " + str(error1)
#            + "\n  tolerance:             " + str(tolerance))
#        
#        ## Fixed Underlying bond (Isin: IT0006527060 IBRD 5 02/05/19)
#        ## maturity occurs on a business day
#
#        fixedBondSchedule2 = Schedule(Date(5,February,2005),
#                                    Date(5,February,2019),
#                                    Period(Annual), bondCalendar,
#                                    Unadjusted, Unadjusted,
#                                    DateGeneration.Backward, False)
#        fixedBond2 = FixedRateBond(settlementDays, self.faceAmount,
#                                               fixedBondSchedule2,
#                                               [0.05],
#                                               Thirty360(Thirty360.BondBasis),
#                                               Following,
#                                               100.0, Date(5,February,2005))
#
#        fixedBond2.setPricingEngine(bondEngine)
#
#        fixedBondPrice2 = fixedBond2.cleanPrice()
#        fixedBondAssetSwap2 = AssetSwap(payFixedRate,
#                                      fixedBond2, fixedBondPrice2,
#                                      self.iborIndex, self.spread,
#                                      Schedule(),
#                                      self.iborIndex.dayCounter(),
#                                      parAssetSwap)
#        fixedBondAssetSwap2.setPricingEngine(swapEngine)
#        fixedBondAssetSwapPrice2 = fixedBondAssetSwap2.fairCleanPrice()
#        error2 = abs(fixedBondAssetSwapPrice2-fixedBondPrice2)
#
#        self.assertFalse(error2>tolerance,  
#            "wrong zero spread asset swap price for fixed bond:"
#            + "\n  bond's clean price:    " + str(fixedBondPrice2)
#            + "\n  asset swap fair price: " + str(fixedBondAssetSwapPrice2)
#            + "\n  error:                 " + str(error2)
#            + "\n  tolerance:             " + str(tolerance))
#        
#
#        ## Zero Coupon bond (Isin: DE0004771662 IBRD 0 12/20/15)
#        ## maturity doesn't occur on a business day
#
#        zeroCpnBond1 = ZeroCouponBond(settlementDays, bondCalendar, self.faceAmount,
#                           Date(20,December,2015),
#                           Following,
#                           100.0, Date(19,December,1985))
#
#        zeroCpnBond1.setPricingEngine(bondEngine)
#
#        zeroCpnBondPrice1 = zeroCpnBond1.cleanPrice()
#        zeroCpnAssetSwap1 = AssetSwap(payFixedRate,
#                                    zeroCpnBond1, zeroCpnBondPrice1,
#                                    self.iborIndex, self.spread,
#                                    Schedule(),
#                                    self.iborIndex.dayCounter(),
#                                    parAssetSwap)
#        zeroCpnAssetSwap1.setPricingEngine(swapEngine)
#        zeroCpnBondAssetSwapPrice1 = zeroCpnAssetSwap1.fairCleanPrice()
#        error8 = abs(cmsBondAssetSwapPrice1-cmsBondPrice1)
#
#        self.assertFalse(error8>tolerance, 
#            "wrong zero spread asset swap price for zero cpn bond:"
#            + "\n  bond's clean price:    " + str(zeroCpnBondPrice1)
#            + "\n  asset swap fair price: " + str(zeroCpnBondAssetSwapPrice1)
#            + "\n  error:                 " + str(error8)
#            + "\n  tolerance:             " + str(tolerance))
#        
#
#        ## Zero Coupon bond (Isin: IT0001200390 ISPIM 0 02/17/28)
#        ## maturity occurs on a business day
#
#        zeroCpnBond2 = ZeroCouponBond(settlementDays, bondCalendar, self.faceAmount,
#                           Date(17,February,2028),
#                           Following,
#                           100.0, Date(17,February,1998))
#
#        zeroCpnBond2.setPricingEngine(bondEngine)
#
#        zeroCpnBondPrice2 = zeroCpnBond2.cleanPrice()
#        zeroCpnAssetSwap2 = AssetSwap(payFixedRate,
#                                    zeroCpnBond2, zeroCpnBondPrice2,
#                                    self.iborIndex, self.spread,
#                                    Schedule(),
#                                    self.iborIndex.dayCounter(),
#                                    parAssetSwap)
#        zeroCpnAssetSwap2.setPricingEngine(swapEngine)
#        zeroCpnBondAssetSwapPrice2 = zeroCpnAssetSwap2.fairCleanPrice()
#        error9 = abs(cmsBondAssetSwapPrice2-cmsBondPrice2)
#
#        self.assertFalse(error9>tolerance, 
#            "wrong zero spread asset swap price for zero cpn bond:"
#            + "\n  bond's clean price:      " + str(zeroCpnBondPrice2)
#            + "\n  asset swap fair price:   " + str(zeroCpnBondAssetSwapPrice2)
#            + "\n  error:                   " + str(error9)
#            + "\n  tolerance:               " + str(tolerance))
#

if __name__ == '__main__':
    print ('testing QuantLib', QuantLib.__version__)
    #testConsistency()
    mytest()
