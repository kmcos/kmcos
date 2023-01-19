module nli_0005
use kind_values
use lattice
use proclist_constants
implicit none
contains
pure function nli_hop_left(cell)
    integer(kind=iint), dimension(4), intent(in) :: cell
    integer(kind=iint) :: nli_hop_left

    select case(get_species(cell + (/-1, 0, 0, default_a/)))
      case default
        nli_hop_left = 0; return
      case(empty)
        select case(get_species(cell + (/0, 0, 0, default_a/)))
          case default
            nli_hop_left = 0; return
          case(Au)
            nli_hop_left = hop_left; return
        end select
    end select

end function nli_hop_left

end module
