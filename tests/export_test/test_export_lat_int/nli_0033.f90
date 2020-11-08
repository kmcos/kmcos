module nli_0033
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_reaction_oxygen_cus_co_bridge_right(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_reaction_oxygen_cus_co_bridge_right

    select case(get_species(cell + (/0, 0, 0, ruo2_cus/)))
      case default
        nli_reaction_oxygen_cus_co_bridge_right = 0; return
      case(oxygen)
        select case(get_species(cell + (/1, 0, 0, ruo2_bridge/)))
          case default
            nli_reaction_oxygen_cus_co_bridge_right = 0; return
          case(co)
            nli_reaction_oxygen_cus_co_bridge_right = reaction_oxygen_cus_co_bridge_right; return
        end select
    end select

end function nli_reaction_oxygen_cus_co_bridge_right

end module
