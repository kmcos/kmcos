module nli_0022
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_oxygen_diffusion_bridge_cus_left(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_oxygen_diffusion_bridge_cus_left

    select case(get_species(cell + (/-1, 0, 0, ruo2_cus/)))
      case default
        nli_oxygen_diffusion_bridge_cus_left = 0; return
      case(empty)
        select case(get_species(cell + (/0, 0, 0, ruo2_bridge/)))
          case default
            nli_oxygen_diffusion_bridge_cus_left = 0; return
          case(oxygen)
            nli_oxygen_diffusion_bridge_cus_left = oxygen_diffusion_bridge_cus_left; return
        end select
    end select

end function nli_oxygen_diffusion_bridge_cus_left

end module
