module nli_0009
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_co_diffusion_cus_bridge_right(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_co_diffusion_cus_bridge_right

    select case(get_species(cell + (/0, 0, 0, ruo2_cus/)))
      case default
        nli_co_diffusion_cus_bridge_right = 0; return
      case(co)
        select case(get_species(cell + (/1, 0, 0, ruo2_bridge/)))
          case default
            nli_co_diffusion_cus_bridge_right = 0; return
          case(empty)
            nli_co_diffusion_cus_bridge_right = co_diffusion_cus_bridge_right; return
        end select
    end select

end function nli_co_diffusion_cus_bridge_right

end module
