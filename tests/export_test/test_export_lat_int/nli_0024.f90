module nli_0024
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_oxygen_diffusion_cus_bridge_left(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_oxygen_diffusion_cus_bridge_left

    select case(get_species(cell + (/0, 0, 0, ruo2_cus/)))
      case default
        nli_oxygen_diffusion_cus_bridge_left = 0; return
      case(oxygen)
        select case(get_species(cell + (/0, 0, 0, ruo2_bridge/)))
          case default
            nli_oxygen_diffusion_cus_bridge_left = 0; return
          case(empty)
            nli_oxygen_diffusion_cus_bridge_left = oxygen_diffusion_cus_bridge_left; return
        end select
    end select

end function nli_oxygen_diffusion_cus_bridge_left

end module
