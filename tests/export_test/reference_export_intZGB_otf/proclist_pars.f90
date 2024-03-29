!  This file was generated by kmcos (kinetic Monte Carlo of Systems)
!  written by Max J. Hoffmann mjhoffmann@gmail.com (C) 2009-2013.
!  The model was written by Juan M. Lorenzi.

!  This file is part of kmcos.
!
!  kmcos is free software; you can redistribute it and/or modify
!  it under the terms of the GNU General Public License as published by
!  the Free Software Foundation; either version 2 of the License, or
!  (at your option) any later version.
!
!  kmcos is distributed in the hope that it will be useful,
!  but WITHOUT ANY WARRANTY; without even the implied warranty of
!  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
!  GNU General Public License for more details.
!
!  You should have received a copy of the GNU General Public License
!  along with kmcos; if not, write to the Free Software
!  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
!  USA
module proclist_pars
use kind_values
use base, only: &
    rates
use proclist_constants
use lattice, only: &
    square, &
    square_default, &
    get_species

implicit none

! User parameters
integer(kind=iint), public :: J_CO_CO = 1
integer(kind=iint), public :: J_O_CO = 2
integer(kind=iint), public :: J_O_O = 3
integer(kind=iint), public :: kDes = 4
integer(kind=iint), public :: yCO = 5
real(kind=rdouble), public, dimension(5) :: userpar

! Constants

! Species masses
character(len=18), parameter, public :: byst_CO_ads = "nr_CO_1nn &
    &nr_O_1nn"
character(len=1), parameter, public :: byst_CO_des = ""
character(len=39), parameter, public :: byst_CO_oxidation_00 = "nr_CO_COnn &
    &nr_O_COnn &
    &nr_CO_Onn &
    &nr_O_Onn"
character(len=39), parameter, public :: byst_CO_oxidation_01 = "nr_CO_COnn &
    &nr_O_COnn &
    &nr_CO_Onn &
    &nr_O_Onn"
character(len=39), parameter, public :: byst_CO_oxidation_02 = "nr_CO_COnn &
    &nr_O_COnn &
    &nr_CO_Onn &
    &nr_O_Onn"
character(len=39), parameter, public :: byst_CO_oxidation_03 = "nr_CO_COnn &
    &nr_O_COnn &
    &nr_CO_Onn &
    &nr_O_Onn"
character(len=1), parameter, public :: byst_O2_des_right = ""
character(len=1), parameter, public :: byst_O2_des_up = ""
character(len=18), parameter, public :: byst_O_ads_00 = "nr_CO_1nn &
    &nr_O_1nn"
character(len=18), parameter, public :: byst_O_ads_01 = "nr_CO_1nn &
    &nr_O_1nn"

contains
subroutine update_user_parameter(param,val)
    integer(kind=iint), intent(in) :: param
    real(kind=rdouble), intent(in) :: val
    userpar(param) = val
end subroutine update_user_parameter

subroutine get_user_parameter(param,val)
    integer(kind=iint), intent(in) :: param
    real(kind=rdouble), intent(out) :: val
    val = userpar(param)
end subroutine get_user_parameter


function gr_CO_ads(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint), dimension(2) :: nr_vars
    real(kind=rdouble) :: gr_CO_ads

    nr_vars(:) = 0
    select case(get_species(cell + (/1, 0, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/0, 1, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/-1, 0, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/0, -1, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select

    gr_CO_ads = rate_CO_ads(nr_vars)
    return

end function gr_CO_ads

function rate_CO_ads(nr_vars)

    integer(kind=iint), dimension(2), intent(in) :: nr_vars

    real(kind=rdouble) :: rate_CO_ads
    rate_CO_ads = rates (CO_ads ) * (userpar(J_O_CO) ** nr_vars(2) ) * (&
    &userpar(J_CO_CO)  ** nr_vars(1) )   

    return

end function rate_CO_ads


function gr_CO_des(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    real(kind=rdouble) :: gr_CO_des


    gr_CO_des = rate_CO_des()
    return

end function gr_CO_des

function rate_CO_des()


    real(kind=rdouble) :: rate_CO_des
    rate_CO_des = rates(CO_des)
    return

end function rate_CO_des


function gr_CO_oxidation_00(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint), dimension(4) :: nr_vars
    real(kind=rdouble) :: gr_CO_oxidation_00

    nr_vars(:) = 0
    select case(get_species(cell + (/0, 1, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/-1, 0, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/0, -1, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/2, 0, 0, square_default/)))
        case(O)
            nr_vars(4) = nr_vars(4) + 1
        case(CO)
            nr_vars(3) = nr_vars(3) + 1
    end select
    select case(get_species(cell + (/1, 1, 0, square_default/)))
        case(O)
            nr_vars(4) = nr_vars(4) + 1
        case(CO)
            nr_vars(3) = nr_vars(3) + 1
    end select
    select case(get_species(cell + (/1, -1, 0, square_default/)))
        case(O)
            nr_vars(4) = nr_vars(4) + 1
        case(CO)
            nr_vars(3) = nr_vars(3) + 1
    end select

    gr_CO_oxidation_00 = rate_CO_oxidation_00(nr_vars)
    return

end function gr_CO_oxidation_00

function rate_CO_oxidation_00(nr_vars)

    integer(kind=iint), dimension(4), intent(in) :: nr_vars

    real(kind=rdouble) :: rate_CO_oxidation_00
    rate_CO_oxidation_00 = rates (CO_oxidation_00 ) * (userpar(J_O_O) &
    &**  (- nr_vars(4) ) ) * (userpar(J_CO_CO) ** (- nr_vars(1) ) ) * (&
    &userpar(J_O_CO)  ** (- nr_vars(2) - nr_vars(3) ) )   

    return

end function rate_CO_oxidation_00


function gr_CO_oxidation_01(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint), dimension(4) :: nr_vars
    real(kind=rdouble) :: gr_CO_oxidation_01

    nr_vars(:) = 0
    select case(get_species(cell + (/1, 0, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/-1, 0, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/0, -1, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/1, 1, 0, square_default/)))
        case(O)
            nr_vars(4) = nr_vars(4) + 1
        case(CO)
            nr_vars(3) = nr_vars(3) + 1
    end select
    select case(get_species(cell + (/0, 2, 0, square_default/)))
        case(O)
            nr_vars(4) = nr_vars(4) + 1
        case(CO)
            nr_vars(3) = nr_vars(3) + 1
    end select
    select case(get_species(cell + (/-1, 1, 0, square_default/)))
        case(O)
            nr_vars(4) = nr_vars(4) + 1
        case(CO)
            nr_vars(3) = nr_vars(3) + 1
    end select

    gr_CO_oxidation_01 = rate_CO_oxidation_01(nr_vars)
    return

end function gr_CO_oxidation_01

function rate_CO_oxidation_01(nr_vars)

    integer(kind=iint), dimension(4), intent(in) :: nr_vars

    real(kind=rdouble) :: rate_CO_oxidation_01
    rate_CO_oxidation_01 = rates (CO_oxidation_01 ) * (userpar(J_O_O) &
    &**  (- nr_vars(4) ) ) * (userpar(J_CO_CO) ** (- nr_vars(1) ) ) * (&
    &userpar(J_O_CO)  ** (- nr_vars(2) - nr_vars(3) ) )   

    return

end function rate_CO_oxidation_01


function gr_CO_oxidation_02(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint), dimension(4) :: nr_vars
    real(kind=rdouble) :: gr_CO_oxidation_02

    nr_vars(:) = 0
    select case(get_species(cell + (/1, 0, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/0, 1, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/0, -1, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/-1, 1, 0, square_default/)))
        case(O)
            nr_vars(4) = nr_vars(4) + 1
        case(CO)
            nr_vars(3) = nr_vars(3) + 1
    end select
    select case(get_species(cell + (/-2, 0, 0, square_default/)))
        case(O)
            nr_vars(4) = nr_vars(4) + 1
        case(CO)
            nr_vars(3) = nr_vars(3) + 1
    end select
    select case(get_species(cell + (/-1, -1, 0, square_default/)))
        case(O)
            nr_vars(4) = nr_vars(4) + 1
        case(CO)
            nr_vars(3) = nr_vars(3) + 1
    end select

    gr_CO_oxidation_02 = rate_CO_oxidation_02(nr_vars)
    return

end function gr_CO_oxidation_02

function rate_CO_oxidation_02(nr_vars)

    integer(kind=iint), dimension(4), intent(in) :: nr_vars

    real(kind=rdouble) :: rate_CO_oxidation_02
    rate_CO_oxidation_02 = rates (CO_oxidation_02 ) * (userpar(J_O_O) &
    &**  (- nr_vars(4) ) ) * (userpar(J_CO_CO) ** (- nr_vars(1) ) ) * (&
    &userpar(J_O_CO)  ** (- nr_vars(2) - nr_vars(3) ) )   

    return

end function rate_CO_oxidation_02


function gr_CO_oxidation_03(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint), dimension(4) :: nr_vars
    real(kind=rdouble) :: gr_CO_oxidation_03

    nr_vars(:) = 0
    select case(get_species(cell + (/1, 0, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/0, 1, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/-1, 0, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/1, -1, 0, square_default/)))
        case(O)
            nr_vars(4) = nr_vars(4) + 1
        case(CO)
            nr_vars(3) = nr_vars(3) + 1
    end select
    select case(get_species(cell + (/-1, -1, 0, square_default/)))
        case(O)
            nr_vars(4) = nr_vars(4) + 1
        case(CO)
            nr_vars(3) = nr_vars(3) + 1
    end select
    select case(get_species(cell + (/0, -2, 0, square_default/)))
        case(O)
            nr_vars(4) = nr_vars(4) + 1
        case(CO)
            nr_vars(3) = nr_vars(3) + 1
    end select

    gr_CO_oxidation_03 = rate_CO_oxidation_03(nr_vars)
    return

end function gr_CO_oxidation_03

function rate_CO_oxidation_03(nr_vars)

    integer(kind=iint), dimension(4), intent(in) :: nr_vars

    real(kind=rdouble) :: rate_CO_oxidation_03
    rate_CO_oxidation_03 = rates (CO_oxidation_03 ) * (userpar(J_O_O) &
    &**  (- nr_vars(4) ) ) * (userpar(J_CO_CO) ** (- nr_vars(1) ) ) * (&
    &userpar(J_O_CO)  ** (- nr_vars(2) - nr_vars(3) ) )   

    return

end function rate_CO_oxidation_03


function gr_O2_des_right(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    real(kind=rdouble) :: gr_O2_des_right


    gr_O2_des_right = rate_O2_des_right()
    return

end function gr_O2_des_right

function rate_O2_des_right()


    real(kind=rdouble) :: rate_O2_des_right
    rate_O2_des_right = rates(O2_des_right)
    return

end function rate_O2_des_right


function gr_O2_des_up(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    real(kind=rdouble) :: gr_O2_des_up


    gr_O2_des_up = rate_O2_des_up()
    return

end function gr_O2_des_up

function rate_O2_des_up()


    real(kind=rdouble) :: rate_O2_des_up
    rate_O2_des_up = rates(O2_des_up)
    return

end function rate_O2_des_up


function gr_O_ads_00(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint), dimension(2) :: nr_vars
    real(kind=rdouble) :: gr_O_ads_00

    nr_vars(:) = 0
    select case(get_species(cell + (/2, 0, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/1, 1, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/0, 1, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/-1, 0, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/0, -1, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/1, -1, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select

    gr_O_ads_00 = rate_O_ads_00(nr_vars)
    return

end function gr_O_ads_00

function rate_O_ads_00(nr_vars)

    integer(kind=iint), dimension(2), intent(in) :: nr_vars

    real(kind=rdouble) :: rate_O_ads_00
    rate_O_ads_00 = rates (O_ads_00 ) * (userpar(J_O_O) ** nr_vars(2) ) &
    &*  (userpar(J_O_CO) ** nr_vars(1) )   

    return

end function rate_O_ads_00


function gr_O_ads_01(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint), dimension(2) :: nr_vars
    real(kind=rdouble) :: gr_O_ads_01

    nr_vars(:) = 0
    select case(get_species(cell + (/1, 0, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/1, 1, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/0, 2, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/-1, 1, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/-1, 0, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select
    select case(get_species(cell + (/0, -1, 0, square_default/)))
        case(O)
            nr_vars(2) = nr_vars(2) + 1
        case(CO)
            nr_vars(1) = nr_vars(1) + 1
    end select

    gr_O_ads_01 = rate_O_ads_01(nr_vars)
    return

end function gr_O_ads_01

function rate_O_ads_01(nr_vars)

    integer(kind=iint), dimension(2), intent(in) :: nr_vars

    real(kind=rdouble) :: rate_O_ads_01
    rate_O_ads_01 = rates (O_ads_01 ) * (userpar(J_O_O) ** nr_vars(2) ) &
    &*  (userpar(J_O_CO) ** nr_vars(1) )   

    return

end function rate_O_ads_01


end module proclist_pars
